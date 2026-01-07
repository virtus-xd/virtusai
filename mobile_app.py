"""
VIRTUS Mobile App - Android/iOS için Kivy tabanlı uygulama
Bu dosya mobil uygulama geliştirmek isteyenler için bir başlangıç noktasıdır.

Kurulum:
pip install kivy plyer buildozer

Android için build:
buildozer init
buildozer -v android debug
"""

try:
    from kivy.app import App
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.button import Button
    from kivy.uix.label import Label
    from kivy.uix.textinput import TextInput
    from kivy.clock import Clock
    from plyer import tts, stt, notification
    KIVY_AVAILABLE = True
except ImportError:
    KIVY_AVAILABLE = False
    print("⚠️  Kivy kurulu değil. Mobil app çalıştırılamıyor.")


if KIVY_AVAILABLE:
    import sys
    sys.path.insert(0, '.')
    from core.ai_brain import AIBrain
    from core.action_executor import ActionExecutor


    class VirtusApp(App):
        """Virtus Mobil Uygulaması"""
        
        def build(self):
            self.title = "VIRTUS AI"
            
            # AI modüllerini başlat
            try:
                self.ai = AIBrain()
                self.executor = ActionExecutor()
            except Exception as e:
                print(f"AI başlatma hatası: {e}")
                self.ai = None
                self.executor = None
            
            # UI
            layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
            
            # Başlık
            title = Label(
                text='VIRTUS AI ASISTAN',
                size_hint=(1, 0.1),
                font_size='24sp',
                bold=True
            )
            layout.add_widget(title)
            
            # Yanıt alanı
            self.response_label = Label(
                text='Merhaba! Ben Virtus.\nSize nasıl yardımcı olabilirim?',
                size_hint=(1, 0.3),
                font_size='18sp',
                halign='center',
                valign='middle'
            )
            self.response_label.bind(size=self.response_label.setter('text_size'))
            layout.add_widget(self.response_label)
            
            # Komut input
            self.command_input = TextInput(
                hint_text='Komutunuzu yazın...',
                size_hint=(1, 0.1),
                multiline=False,
                font_size='16sp'
            )
            self.command_input.bind(on_text_validate=self.process_text_command)
            layout.add_widget(self.command_input)
            
            # Butonlar
            button_layout = BoxLayout(size_hint=(1, 0.15), spacing=10)
            
            # Sesli komut butonu
            self.voice_btn = Button(
                text='🎤 Sesli Komut',
                font_size='16sp',
                background_color=(0.2, 0.6, 1, 1)
            )
            self.voice_btn.bind(on_press=self.start_voice_command)
            button_layout.add_widget(self.voice_btn)
            
            # Metin gönder butonu
            send_btn = Button(
                text='📝 Gönder',
                font_size='16sp',
                background_color=(0.3, 0.7, 0.3, 1)
            )
            send_btn.bind(on_press=self.process_text_command)
            button_layout.add_widget(send_btn)
            
            layout.add_widget(button_layout)
            
            # Durum
            self.status_label = Label(
                text='Hazır',
                size_hint=(1, 0.05),
                font_size='14sp',
                color=(0.7, 0.7, 0.7, 1)
            )
            layout.add_widget(self.status_label)
            
            return layout
        
        def start_voice_command(self, instance):
            """Sesli komut dinle"""
            try:
                self.status_label.text = '🎤 Dinliyorum...'
                self.voice_btn.disabled = True
                
                # Android ses tanıma
                def on_result(text):
                    if text:
                        self.command_input.text = text[0]
                        self.process_command(text[0])
                    self.voice_btn.disabled = False
                    self.status_label.text = 'Hazır'
                
                stt.start()
                stt.bind(on_result=on_result)
                
            except Exception as e:
                self.status_label.text = f'❌ Hata: {e}'
                self.voice_btn.disabled = False
        
        def process_text_command(self, instance):
            """Metin komutunu işle"""
            command = self.command_input.text.strip()
            if command:
                self.process_command(command)
                self.command_input.text = ''
        
        def process_command(self, command):
            """Komutu AI ile işle"""
            if not self.ai:
                self.response_label.text = '❌ AI modülü hazır değil'
                return
            
            try:
                self.status_label.text = '🤔 İşleniyor...'
                
                # AI ile işle
                result = self.ai.process_command(command)
                
                # Yanıtı göster
                response = result.get('response', 'Yanıt alınamadı')
                self.response_label.text = response
                
                # TTS ile söyle
                try:
                    tts.speak(response)
                except:
                    pass
                
                # Aksiyonu çalıştır
                if self.executor:
                    self.executor.execute(result)
                
                # Bildirim göster
                notification.notify(
                    title='Virtus',
                    message=response,
                    timeout=3
                )
                
                self.status_label.text = '✅ Tamamlandı'
                
            except Exception as e:
                error_msg = f'❌ Hata: {str(e)}'
                self.response_label.text = error_msg
                self.status_label.text = 'Hata'


    def main():
        """Mobil app başlat"""
        if not KIVY_AVAILABLE:
            print("Kivy kurulu değil!")
            print("Kurulum: pip install kivy plyer")
            return
        
        VirtusApp().run()


    if __name__ == '__main__':
        main()

else:
    def main():
        print("⚠️  Kivy bulunamadı!")
        print("\nMobil app için gerekli paketler:")
        print("  pip install kivy plyer buildozer")
        print("\nAndroid build için:")
        print("  buildozer init")
        print("  buildozer -v android debug")
