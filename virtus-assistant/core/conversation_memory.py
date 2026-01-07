"""
Konuşma Hafızası ve Bağlam Yönetimi
- Geçmiş konuşmaları hatırlar
- Bağlam analizini yapar
- Kullanıcı profilini öğrenir
- Kişiselleştirilmiş yanıtlar verir
"""
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


class ConversationMemory:
    """Akıllı konuşma hafızası - JARVIS tarzı"""
    
    def __init__(self, user_name: str = "Kullanıcı"):
        self.user_name = user_name
        self.conversation_history: List[Dict] = []
        self.long_term_memory: Dict = {}
        self.user_profile: Dict = {}
        self.current_context: Dict = {}
        
        # Dosya yolları
        self.data_dir = Path('data/memory')
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.conversation_file = self.data_dir / 'conversation_history.json'
        self.long_term_file = self.data_dir / 'long_term_memory.json'
        self.profile_file = self.data_dir / 'user_profile.json'
        
        # Hafızayı yükle
        self._load_memory()
        
        logger.info(f"💾 Hafıza sistemi yüklendi - {len(self.conversation_history)} geçmiş konuşma")
    
    def add_interaction(self, user_input: str, assistant_response: str, 
                       intent: str = None, entities: Dict = None):
        """
        Yeni bir etkileşim ekle
        
        Args:
            user_input: Kullanıcının söylediği
            assistant_response: Asistanın yanıtı
            intent: Komutun amacı (örn: search, open_app)
            entities: Çıkarılan varlıklar (örn: {"app": "chrome"})
        """
        interaction = {
            'timestamp': datetime.now().isoformat(),
            'user': user_input,
            'assistant': assistant_response,
            'intent': intent,
            'entities': entities or {}
        }
        
        # Konuşma geçmişine ekle
        self.conversation_history.append(interaction)
        
        # Son 100 konuşmayı tut (performans için)
        if len(self.conversation_history) > 100:
            self.conversation_history = self.conversation_history[-100:]
        
        # Bağlamı güncelle
        self._update_context(interaction)
        
        # Uzun dönem hafızayı güncelle
        self._update_long_term_memory(interaction)
        
        # Profili güncelle
        self._update_user_profile(interaction)
        
        # Kaydet
        self._save_memory()
        
        logger.debug(f"💬 Etkileşim kaydedildi: {user_input[:30]}...")
    
    def _update_context(self, interaction: Dict):
        """Mevcut konuşma bağlamını güncelle"""
        # Son konuşulan konuyu sakla
        if interaction['intent'] == 'information':
            entities = interaction.get('entities', {})
            query = entities.get('query', '') or interaction['user']
            
            # Anahtar kelimeleri çıkar
            keywords = self._extract_keywords(query)
            self.current_context['last_topic'] = keywords
            self.current_context['last_query'] = query
            self.current_context['last_time'] = interaction['timestamp']
        
        elif interaction['intent'] == 'open_app':
            app_name = interaction.get('entities', {}).get('app_name', '')
            self.current_context['last_app'] = app_name
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Metinden anahtar kelimeleri çıkar"""
        # Basit keyword extraction (gelişmiş NLP eklenebilir)
        text = text.lower()
        
        # Gereksiz kelimeleri çıkar
        stop_words = {'nedir', 'ne', 'nasıl', 'kaç', 'kim', 'nerede', 
                     'ne zaman', 'hangi', 'bir', 'bu', 'şu', 'mi', 'mı', 
                     'mu', 'mü', 'için', 'ile', 've', 'veya', 'ama'}
        
        words = text.split()
        keywords = [w for w in words if w not in stop_words and len(w) > 2]
        
        return keywords[:5]  # İlk 5 anahtar kelime
    
    def _update_long_term_memory(self, interaction: Dict):
        """Uzun dönem hafızayı güncelle - önemli bilgileri sakla"""
        # Konu frekansı
        if interaction['intent'] == 'information':
            query = interaction['user'].lower()
            keywords = self._extract_keywords(query)
            
            for keyword in keywords:
                if keyword not in self.long_term_memory:
                    self.long_term_memory[keyword] = {
                        'count': 0,
                        'first_asked': interaction['timestamp'],
                        'last_asked': interaction['timestamp']
                    }
                
                self.long_term_memory[keyword]['count'] += 1
                self.long_term_memory[keyword]['last_asked'] = interaction['timestamp']
    
    def _update_user_profile(self, interaction: Dict):
        """Kullanıcı profilini güncelle - tercihler, alışkanlıklar"""
        # Sık kullanılan uygulamalar
        if interaction['intent'] == 'open_app':
            app_name = interaction.get('entities', {}).get('app_name', '')
            if app_name:
                if 'favorite_apps' not in self.user_profile:
                    self.user_profile['favorite_apps'] = {}
                
                if app_name not in self.user_profile['favorite_apps']:
                    self.user_profile['favorite_apps'][app_name] = 0
                
                self.user_profile['favorite_apps'][app_name] += 1
        
        # Sık sorulan sorular
        if interaction['intent'] == 'information':
            if 'question_count' not in self.user_profile:
                self.user_profile['question_count'] = 0
            self.user_profile['question_count'] += 1
        
        # Toplam etkileşim
        if 'total_interactions' not in self.user_profile:
            self.user_profile['total_interactions'] = 0
        self.user_profile['total_interactions'] += 1
    
    def get_context_for_ai(self, current_query: str) -> str:
        """
        AI için bağlam bilgisi oluştur
        
        Returns:
            AI'ya gönderilecek bağlam metni
        """
        context_parts = []
        
        # Kullanıcı profili
        if self.user_profile:
            total = self.user_profile.get('total_interactions', 0)
            if total > 0:
                context_parts.append(f"Kullanıcı bilgisi: {total} önceki etkileşim.")
        
        # Son konuşma bağlamı
        if self.current_context.get('last_topic'):
            keywords = ', '.join(self.current_context['last_topic'])
            context_parts.append(f"Son konuşulan: {keywords}")
        
        # Son 3 etkileşim (kısa özet)
        recent = self.conversation_history[-3:]
        if recent:
            context_parts.append("\nSon konuşmalar:")
            for i, conv in enumerate(recent, 1):
                user_msg = conv['user'][:50]
                context_parts.append(f"{i}. Kullanıcı: {user_msg}")
        
        # Sık kullanılan uygulamalar
        fav_apps = self.user_profile.get('favorite_apps', {})
        if fav_apps:
            top_apps = sorted(fav_apps.items(), key=lambda x: x[1], reverse=True)[:3]
            apps_str = ', '.join([app for app, _ in top_apps])
            context_parts.append(f"Sık kullanılan uygulamalar: {apps_str}")
        
        # Mevcut sorgu ile ilgili önceki konuşmalar
        related = self._find_related_conversations(current_query)
        if related:
            context_parts.append("\nİlgili önceki konuşmalar:")
            for conv in related[:2]:  # En fazla 2 tane
                context_parts.append(f"- {conv['user'][:50]} → {conv['assistant'][:50]}")
        
        return "\n".join(context_parts)
    
    def _find_related_conversations(self, query: str, limit: int = 3) -> List[Dict]:
        """Sorgu ile ilgili önceki konuşmaları bul"""
        query_keywords = set(self._extract_keywords(query.lower()))
        
        if not query_keywords:
            return []
        
        scored_convs = []
        
        for conv in self.conversation_history[-20:]:  # Son 20 konuşmayı kontrol et
            conv_keywords = set(self._extract_keywords(conv['user'].lower()))
            
            # Ortak kelime sayısı
            common = query_keywords.intersection(conv_keywords)
            if common:
                score = len(common)
                scored_convs.append((score, conv))
        
        # Skora göre sırala
        scored_convs.sort(reverse=True, key=lambda x: x[0])
        
        return [conv for score, conv in scored_convs[:limit]]
    
    def get_summary(self) -> Dict:
        """Hafıza özeti"""
        return {
            'total_conversations': len(self.conversation_history),
            'user_profile': self.user_profile,
            'top_topics': sorted(
                self.long_term_memory.items(), 
                key=lambda x: x[1]['count'], 
                reverse=True
            )[:5],
            'current_context': self.current_context
        }
    
    def clear_context(self):
        """Mevcut bağlamı temizle (yeni konu)"""
        self.current_context = {}
        logger.info("🔄 Bağlam temizlendi")
    
    def _save_memory(self):
        """Hafızayı diske kaydet"""
        try:
            # Konuşma geçmişi
            with open(self.conversation_file, 'w', encoding='utf-8') as f:
                json.dump(self.conversation_history, f, ensure_ascii=False, indent=2)
            
            # Uzun dönem hafıza
            with open(self.long_term_file, 'w', encoding='utf-8') as f:
                json.dump(self.long_term_memory, f, ensure_ascii=False, indent=2)
            
            # Kullanıcı profili
            with open(self.profile_file, 'w', encoding='utf-8') as f:
                json.dump(self.user_profile, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            logger.error(f"Hafıza kaydetme hatası: {e}")
    
    def _load_memory(self):
        """Hafızayı diskten yükle"""
        try:
            # Konuşma geçmişi
            if self.conversation_file.exists():
                with open(self.conversation_file, 'r', encoding='utf-8') as f:
                    self.conversation_history = json.load(f)
            
            # Uzun dönem hafıza
            if self.long_term_file.exists():
                with open(self.long_term_file, 'r', encoding='utf-8') as f:
                    self.long_term_memory = json.load(f)
            
            # Kullanıcı profili
            if self.profile_file.exists():
                with open(self.profile_file, 'r', encoding='utf-8') as f:
                    self.user_profile = json.load(f)
                    
        except Exception as e:
            logger.error(f"Hafıza yükleme hatası: {e}")


# Test
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("Testing Conversation Memory...\n")
    
    memory = ConversationMemory()
    
    # Örnek etkileşimler
    memory.add_interaction(
        "Anıtkabir'i yılda kaç kişi ziyaret ediyor?",
        "Anıtkabir'i yılda yaklaşık 10 milyon kişi ziyaret ediyor.",
        intent='information',
        entities={'query': 'Anıtkabir ziyaretçi sayısı'}
    )
    
    memory.add_interaction(
        "Peki ne zaman inşa edildi?",
        "Anıtkabir 1944-1953 yılları arasında inşa edildi.",
        intent='information',
        entities={'query': 'Anıtkabir inşa tarihi'}
    )
    
    # Bağlam testi
    context = memory.get_context_for_ai("Kim tasarladı?")
    print("Bağlam:")
    print(context)
    print("\nÖzet:")
    print(json.dumps(memory.get_summary(), indent=2, ensure_ascii=False))
