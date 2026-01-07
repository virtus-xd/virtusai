"""
AI Brain - Google Gemini ile komut işleme
"""
import json
import logging
from config.settings import GOOGLE_API_KEY, ASSISTANT_NAME

# Yeni veya eski Gemini API
try:
    import google.genai as genai
    GENAI_NEW = True
except ImportError:
    try:
        import google.generativeai as genai
        GENAI_NEW = False
    except ImportError:
        raise ImportError("Lütfen 'pip install google-genai' veya 'pip install google-generativeai' yürütün")

logger = logging.getLogger(__name__)


class AIBrain:
    def __init__(self):
        self.conversation_history = []
        self.system_prompt = self._create_system_prompt()
        
        if GENAI_NEW:
            # Yeni API (google-genai)
            self.client = genai.Client(api_key=GOOGLE_API_KEY)
            self.model_name = 'gemini-2.0-flash-exp'
            logger.info("Google Genai (yeni API) kullanılıyor")
        else:
            # Eski API (google-generativeai)
            genai.configure(api_key=GOOGLE_API_KEY)
            self.model = genai.GenerativeModel('gemini-pro')
            logger.info("Google Generative AI (eski API) kullanılıyor")
    
    def _create_system_prompt(self):
        """Virtus'un kişiliği ve yetenekleri"""
        return f"""Sen {ASSISTANT_NAME}, kullanıcının kişisel AI asistanısın. JARVIS gibi, yetenekli ve profesyonel bir asistansın.

YETENEKLER:
1. Telefon araması yapma
2. Uygulama açma/kapatma
3. Sistem kontrolü (ses, ekran parlaklığı, vb.)
4. Web araması
5. Dosya işlemleri
6. Bilgi sorgulama
7. Hesaplama
8. Zamanlayıcı ve hatırlatıcılar
9. E-posta gönderme
10. Müzik kontrolü

GÖREVİN:
Kullanıcının komutunu anla ve JSON formatında döndür:

{{
    "intent": "komut_türü",
    "action": "yapılacak_işlem",
    "parameters": {{
        "param1": "değer1"
    }},
    "response": "kullanıcıya_verilecek_yanıt"
}}

INTENT TÜRLERİ:
- call: Arama yap
- open_app: Uygulama aç
- close_app: Uygulama kapat
- search: Web'de ara
- file_operation: Dosya işlemi
- system_control: Sistem ayarı
- information: Bilgi ver
- calculation: Hesaplama
- reminder: Hatırlatıcı
- email: E-posta
- music: Müzik kontrolü
- chat: Sohbet et

ÖRNEKLER:

Kullanıcı: "Mehmet'i ara"
Yanıt: {{"intent": "call", "action": "make_call", "parameters": {{"contact": "Mehmet"}}, "response": "Mehmet'i arıyorum."}}

Kullanıcı: "Chrome'u aç"
Yanıt: {{"intent": "open_app", "action": "open_application", "parameters": {{"app_name": "chrome"}}, "response": "Chrome açılıyor."}}

Kullanıcı: "Hava durumu nasıl?"
Yanıt: {{"intent": "information", "action": "get_weather", "parameters": {{}}, "response": "Hava durumunu kontrol ediyorum."}}

Kullanıcı: "5+7 kaç eder?"
Yanıt: {{"intent": "calculation", "action": "calculate", "parameters": {{"expression": "5+7"}}, "response": "5 artı 7 eşittir 12."}}

KURAL: Her zaman geçerli bir JSON döndür. Türkçe ve kibar ol."""

    def process_command(self, command_text):
        """
        Komutu işle ve aksiyon al
        
        Args:
            command_text (str): Kullanıcı komutu
            
        Returns:
            dict: Intent, action ve parametreler
        """
        try:
            # Prompt oluştur
            prompt = f"{self.system_prompt}\n\nKullanıcı: {command_text}\nYanıt (JSON):"
            
            # Gemini'ye gönder
            if GENAI_NEW:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt
                )
                response_text = response.text
            else:
                response = self.model.generate_content(prompt)
                response_text = response.text
            
            # JSON parse et
            # Gemini bazen ```json ile sarabilir, temizle
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0].strip()
            elif '```' in response_text:
                response_text = response_text.split('```')[1].split('```')[0].strip()
            
            result = json.loads(response_text)
            
            logger.info(f"🧠 AI Response: {result}")
            
            # Konuşma geçmişine ekle
            self.conversation_history.append({
                'user': command_text,
                'assistant': result.get('response', '')
            })
            
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parse hatası: {e}")
            logger.error(f"Raw response: {response_text}")
            return {
                'intent': 'error',
                'action': 'none',
                'parameters': {},
                'response': 'Komutu anlayamadım, tekrar eder misiniz?'
            }
            
        except Exception as e:
            logger.error(f"AI Brain error: {e}")
            return {
                'intent': 'error',
                'action': 'none',
                'parameters': {},
                'response': 'Bir hata oluştu, lütfen tekrar deneyin.'
            }
    
    def chat(self, message):
        """Sohbet modu - JSON formatı olmadan"""
        try:
            # Konuşma geçmişi ile context oluştur
            context = "\n".join([
                f"Kullanıcı: {h['user']}\n{ASSISTANT_NAME}: {h['assistant']}"
                for h in self.conversation_history[-5:]  # Son 5 mesaj
            ])
            
            prompt = f"Sen {ASSISTANT_NAME}, yardımcı bir AI asistanısın.\n\n{context}\n\nKullanıcı: {message}\n{ASSISTANT_NAME}:"
            
            response = self.model.generate_content(prompt)
            response_text = response.text
            
            self.conversation_history.append({
                'user': message,
                'assistant': response_text
            })
            
            return response_text
            
        except Exception as e:
            logger.error(f"Chat error: {e}")
            return "Üzgünüm, şu an yanıt veremiyorum."
