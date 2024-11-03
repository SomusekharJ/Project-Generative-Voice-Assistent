import os
import google.generativeai as genai
import speech_recognition as sr
import pyttsx3
import threading

# Configure the API key
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Configure the text-to-speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 150)  # Adjust the rate if needed

# Configure the speech recognizer
recognizer = sr.Recognizer()

# Create the model with configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 1024,
    "response_mime_type": "text/plain",
}

# Initialize the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Start a chat session with an empty history
chat_session = model.start_chat(history=[])

# Personalized responses for specific questions
personal_responses = {
    "who are you": "I am Ultron, your personal assistant.",
    "what is your name": "My name is Ultron.",
    "who built you": "I was built by SomuSekhar J.",
    "what are you": "I am Ultron, an assistant built to help you with various tasks.",
    "tell me about yourself": "I am Ultron, created by SomuSekhar J to assist and answer your queries."
}

def get_voice_input():
    """Continuously listen for voice input until Enter is pressed."""
    print("Listening... Press Enter to stop listening and process the question.")
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        while True:
            try:
                audio = recognizer.listen(source)
                user_input = recognizer.recognize_google(audio)
                print("You (voice):", user_input)
                return user_input
            except sr.UnknownValueError:
                print("Listening...")  # Continue listening if speech was not understood
            except sr.RequestError:
                print("Error with recognition service; check internet connection.")
                engine.say("Error with recognition service; check internet connection.")
                engine.runAndWait()
                return None

def speak_text(response_text):
    """Speak text with the option to interrupt by pressing 's'."""
    def stop_speech():
        """Stop the speech output if 's' is pressed."""
        input("Press 's' and Enter to stop reading.")
        engine.stop()
        print("Reading stopped.")

    # Start a thread to listen for the stop input
    stop_thread = threading.Thread(target=stop_speech)
    stop_thread.start()

    # Start reading the response text
    engine.say(response_text)
    engine.runAndWait()

def assistant():
    """Runs the assistant, allowing input by text or voice."""
    while True:
        mode = input("Choose input mode: Type 'text' for text input or 'voice' for voice input: ").strip().lower()

        if mode == "text":
            user_input = input("Enter your question: ")
        elif mode == "voice":
            input("Press Enter when you are ready to start speaking.")
            user_input = get_voice_input()
            if user_input is None:
                continue  # Retry if there was an error in voice input
        elif mode == "exit":
            print("Thank You , Goodbye!")
            break
        else:
            print("Invalid input mode. Please type 'text' or 'voice' or 'exit'.")
            continue

        # Check if the input matches any personalized response
        lower_input = user_input.lower()
        response_text = personal_responses.get(lower_input, None)
        
        # If no personal response is matched, send the input to the AI model
        if not response_text:
            print("Processing your question...")
            response = chat_session.send_message(user_input)
            response_text = response.text

        # Print and speak the response, with the option to interrupt reading
        print("ULTRON:", response_text)
        speak_text(response_text)

# Start the assistant
assistant()
