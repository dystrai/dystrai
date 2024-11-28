import comtypes.client

def main():
    # Initialize SAPI.SpVoice
    sapi_voice = comtypes.client.CreateObject("SAPI.SpVoice")
    
    # Get available voices
    voices = sapi_voice.GetVoices()
    print("Vozes disponíveis:")
    for i in range(voices.Count):
        print(f"{i}: {voices.Item(i).GetDescription()}")
    
    # Select a voice
    try:
        voice_index = int(input("Entre o número da voz que você deseja usar: "))
        sapi_voice.Voice = voices.Item(voice_index)
    except (ValueError, IndexError):
        print("Seleção inválida. Usarei a voz padrão.")
    
    # Adjust speaking rate
    print(f"Current speaking rate: {sapi_voice.Rate}")
    new_rate = input("Entre com a taxa da fala (de -10 a 10, padrão 0): ")
    if new_rate.isdigit() or (new_rate.startswith('-') and new_rate[1:].isdigit()):
        sapi_voice.Rate = int(new_rate)
    else:
        print("Entrada inválida. Mantendo a taxa padrão atual.")
    
    # Enter text to speak
    print("Entre com o texto a ser falado. Digite 'exit' para sair.")
    while True:
        text = input(">>> ")
        if text.lower() == 'exit':
            print("Exiting TTS.")
            break
        sapi_voice.Speak(text)

if __name__ == "__main__":
    main()
