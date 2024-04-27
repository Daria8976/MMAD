import replicate
import os
def ADGenerate(vision_prompt_path,audio_prompt_path):
    # Movie Clip Contextual Alignment & Actor-tracking-aware Story Linking
    with open(vision_prompt_path, "r") as file:
        for line in file:
            if line.startswith("videocaption:"):
                videocaption = line.split("videocaption: ")[1].strip()
                print("videocaption",videocaption)
            elif line.startswith("previous:"):
                if len(line.split("previous: ")) > 1:
                    previous = line.split("previous: ")[1].strip()
                    print("previous", previous)
                else:
                    previous = ""
            elif line.startswith("actor:"):
                actor = line.split("actor: ")[1].strip()
                print("actor",actor)
    
    # Audio-aware Feature Enhancing
    with open(audio_prompt_path, "r") as file:
        for line in file:
            if line.startswith("emotion:"):
                emotion = line.split("emotion: ")[1].strip()
                print("emotion",emotion)
            elif line.startswith("events:"):
                events = line.split("events: ")[1].strip()
                print("events",events)
            
    prompt=f"1.Scene Description: {videocaption} 2.Character dialog provides key information: {previous} 3.The names of the people in the video:{actor} 4.The background music provides the emotion of:{emotion} 5.this audio contains sound events: {events}-------Please combine the above information to generate a 20-word descriptive sentence, Don't start with “In the video”, just describe the content of the video."
    print("prompt:",prompt)
    # # llama
    #Set the REPLICATE_API_TOKEN environment variable
    os.environ["REPLICATE_API_TOKEN"] = "your_api_token_here"
    input = {
        "top_p": 1,
        "prompt": prompt,
        "temperature": 0.5,
        "system_prompt": "You are a professional accessible movie narration generation assistant, and your answers help blind people understand the visual information of the movie.",
        "max_new_tokens": 500
    }

    for output in replicate.stream(
        "meta/llama-2-70b-chat",
        input=input
    ):
        print("output:", output, end="")

if __name__ == '__main__':
    ADGenerate(vision_prompt_path='Example/prompt/vision.txt',audio_prompt_path='Example/prompt/audio.txt')
