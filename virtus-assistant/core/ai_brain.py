"""
AI Brain - Google Gemini ile Akıllı Komut İşleme
+ Konuşma hafızası
+ Web araştırması
+ Bağlam analizi
"""
import json
import logging
import requests
from bs4 import BeautifulSoup
from config.settings import GOOGLE_API_KEY, ASSISTANT_NAME

# Gemini API
try:
    import google.genai as genai
    GENAI_NEW = True
except ImportError:
    try:
        import google.generativeai as genai
        GENAI_NEW = False
    except ImportError:
        raise ImportError("Google Gemini API kurulu değil")

logger = logging.getLogger(__name__)


class AIBrainEnhanced:
    """Gelişmiş AI Brain - Hafızalı ve Araştırmacı"""
    
    def __init__(self, memory=None):
        self.memory = memory
        self.system_prompt = self._create_system_prompt()
        
        # Gemini'yi başlat
        if GENAI_NEW:
            self.client = genai.Client(api_key=GOOGLE_API_KEY)
            self.model_name = 'gemini-2.0-flash-exp'
            logger.info("Google Genai (yeni API) kullanılıyor")
        else:
            genai.configure(api_key=GOOGLE_API_KEY)
            self.model = genai.GenerativeModel('gemini-pro')
            logger.info("Google Generative AI (eski API) kullanılıyor")
    
    def _create_system_prompt(self):
        """Virtus'un kişiliği ve yetenekleri"""
        return f"""Sen {ASSISTANT_NAME}, kullanıcının kişisel AI asistanısın. JARVIS gibi akıllı, bağlama duyarlı ve öğrenen bir asistansın.

ÖNEMLİ ÖZELLİKLER:
- Konuşma geçmişini hatırlarsın
- Bağlamı anlarsın (kullanıcı "peki" dediğinde önceki konuyu bilirsin)
- Bilmediğin şeyleri araştırırsın
- Kişiselleştirilmiş yanıtlar verirsin

YETENEKLER:
1. Telefon araması yapma
2. Uygulama açma/kapatma
3. Sistem kontrolü (ses, ekran, vb.)
4. Web araması ve bilgi toplama
5. Dosya işlemleri
6. Hesaplama
7. Hatırlatıcılar
8. E-posta
9. Müzik kontrolü

ARAŞTIRMA KURALI:
Eğer bir sorunun cevabını BİLMİYORSAN:
- "action": "web_search" kullan
- "response" alanında: "İzninizle araştırıyorum..."
- Sonra gerçek cevabı ver

GÖREVİN:
Kullanıcının komutunu anla ve JSON formatında döndür:

{{
    "intent": "komut_türü",
    "action": "yapılacak_işlem",
    "parameters": {{
        "param1": "değer1"
    }},
    "response": "kullanıcıya_verilecek_yanıt",
    "needs_research": true/false
}}

INTENT TÜRLERİ:
- call: Arama yap
- open_app: Uygulama aç
- close_app: Uygulama kapat
- search: Web'de ara
- file_operation: Dosya işlemi
- system_control: Sistem ayarı
- information: Bilgi ver (araştırma gerekebilir)
- calculation: Hesaplama
- reminder: Hatırlatıcı
- email: E-posta
- music: Müzik kontrolü
- chat: Sohbet et

BAĞLAM KURALI:
Kullanıcı belirsiz bir şey dediğinde (örn: "peki ne zaman?", "kim yaptı?", "kaç?") 
SON KONUŞULAN KONU ile ilişkilendir.

ÖRNEKLER:

Kullanıcı: "Mehmet'i ara"
Yanıt: {{"intent": "call", "action": "make_call", "parameters": {{"contact": "Mehmet"}}, "response": "Mehmet'i arıyorum.", "needs_research": false}}

Kullanıcı: "Chrome'u aç"
Yanıt: {{"intent": "open_app", "action": "open_application", "parameters": {{"app_name": "chrome"}}, "response": "Chrome açılıyor.", "needs_research": false}}

Kullanıcı: "Anıtkabir'i yılda kaç kişi ziyaret ediyor?"
Yanıt: {{"intent": "information", "action": "web_search", "parameters": {{"query": "Anıtkabir yıllık ziyaretçi sayısı"}}, "response": "Anıtkabir'in ziyaretçi sayısını araştırıyorum...", "needs_research": true}}

Kullanıcı: "Peki ne zaman inşa edildi?" (önceki soru Anıtkabir hakkındaydı)
Yanıt: {{"intent": "information", "action": "web_search", "parameters": {{"query": "Anıtkabir inşa tarihi"}}, "response": "Anıtkabir'in inşa tarihini araştırıyorum...", "needs_research": true}}

Kullanıcı: "5+7 kaç eder?"
Yanıt: {{"intent": "calculation", "action": "calculate", "parameters": {{"expression": "5+7"}}, "response": "5 artı 7 eşittir 12.", "needs_research": false}}

KURAL: Her zaman geçerli bir JSON döndür. Türkçe ve profesyonel ol."""

    def process_command(self, command_text, context=None):
        """
        Komutu işle - bağlam ve hafıza ile
        
        Args:
            command_text: Kullanıcı komutu
            context: Konuşma bağlamı (opsiyonel)
            
        Returns:
            dict: Intent, action ve parametreler
        """
        try:
            # Bağlam ekle (varsa)
            full_prompt = self.system_prompt
            
            if context:
                full_prompt += f"\n\nÖNCEKİ BAĞLAM:\n{context}\n"
            
            full_prompt += f"\n\nKullanıcı: {command_text}\nYanıt (JSON):"
            
            # Gemini'ye gönder
            if GENAI_NEW:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=full_prompt
                )
                response_text = response.text
            else:
                response = self.model.generate_content(full_prompt)
                response_text = response.text
            
            # JSON parse et
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0].strip()
            elif '```' in response_text:
                response_text = response_text.split('```')[1].split('```')[0].strip()
            
            result = json.loads(response_text)
            
            # Araştırma gerekiyorsa yap
            if result.get('needs_research') and result.get('action') == 'web_search':
                query = result['parameters'].get('query', command_text)
                research_result = self._web_research(query)
                
                if research_result:
                    # AI'ya araştırma sonucunu ver, gerçek cevabı oluştursun
                    result['response'] = self._generate_answer_from_research(
                        command_text, 
                        research_result
                    )
            
            logger.info(f"🧠 AI Response: {result.get('intent')} - {result.get('response', '')[:50]}...")
            
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parse hatası: {e}")
            logger.error(f"Raw response: {response_text}")
            return {
                'intent': 'error',
                'action': 'none',
                'parameters': {},
                'response': 'Komutu anlayamadım, tekrar eder misiniz?',
                'needs_research': False
            }
            
        except Exception as e:
            logger.error(f"AI Brain error: {e}")
            return {
                'intent': 'error',
                'action': 'none',
                'parameters': {},
                'response': 'Bir hata oluştu, lütfen tekrar deneyin.',
                'needs_research': False
            }
    
    def _web_research(self, query: str) -> str:
        """Web'de araştırma yap ve sonuçları getir"""
        try:
            logger.info(f"🔍 Araştırılıyor: {query}")
            
            # Google'da ara
            search_url = f"https://www.google.com/search?q={query}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(search_url, headers=headers, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Featured snippet (direkt cevap) bul
            featured = soup.find('div', class_='hgKElc')
            if featured:
                return featured.get_text(strip=True)
            
            # Knowledge panel bul
            knowledge = soup.find('div', class_='kno-rdesc')
            if knowledge:
                return knowledge.get_text(strip=True)[:500]
            
            # İlk paragrafları topla
            results = []
            for div in soup.find_all('div', class_='VwiC3b'):
                text = div.get_text(strip=True)
                if text and len(text) > 50:
                    results.append(text)
                    if len(results) >= 3:
                        break
            
            if results:
                return ' '.join(results)[:800]
            
            return None
            
        except Exception as e:
            logger.error(f"Web araştırma hatası: {e}")
            return None
    
    def _generate_answer_from_research(self, question: str, research_data: str) -> str:
        """Araştırma sonucundan cevap oluştur"""
        try:
            prompt = f"""Aşağıdaki soru ve araştırma sonucuna dayanarak kısa, öz ve doğru bir cevap ver.

Soru: {question}

Araştırma Sonucu:
{research_data}

KURAL: 
- 1-2 cümle ile özetle
- Doğrudan cevapla
- Kaynaktan kopyalama, kendi cümlelerinle açıkla
- Türkçe konuş

Cevap:"""

            if GENAI_NEW:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt
                )
                answer = response.text.strip()
            else:
                response = self.model.generate_content(prompt)
                answer = response.text.strip()
            
            logger.info(f"✅ Araştırma cevabı oluşturuldu")
            return answer
            
        except Exception as e:
            logger.error(f"Cevap oluşturma hatası: {e}")
            return "Araştırma yaptım ama cevabı özetleyemedim. Lütfen tekrar deneyin."


# Test
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("Testing Enhanced AI Brain...\n")
    
    ai = AIBrainEnhanced()
    
    # Test 1: Basit komut
    result = ai.process_command("Chrome'u aç")
    print(f"Test 1: {result}\n")
    
    # Test 2: Araştırma gerektiren soru
    result = ai.process_command("Anıtkabir'i yılda kaç kişi ziyaret ediyor?")
    print(f"Test 2: {result}\n")