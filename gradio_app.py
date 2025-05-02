#voicebot UI with Gradio
import os
import gradio as gr


from brain_of_the_doctor import encode_image, analyze_image_with_query
from voice_of_the_patient import record_audio,transcribe_with_groq
from voice_of_the_doctor import text_to_speech_with_gtts,text_to_speech_with_elevenlabs


system_prompts="""You have to act as a professional doctor, i know yor are not but this is for learning purpose.
what's in this image?.Do you find anything wrong with it medically?
If you make a differential,support some remedies for time. do not add any numbers or special chracters in your response.
Your response should be in one long paragraph.Also always answer as if you are answering to a real person.
donot say 'In the image I see " but say 'eith what i see, i think you have..."
donot respond as an AI modle in markdown, your answer should mimic that of an actual doctor not an AI bot,
keep your answer concise (max 2 sentences).No preamble, start your answer right away please

"""


def process_inputs(audio_filepath,image_filepath):
    speech_to_text_output = transcribe_with_groq(GROQ_API_KEY=os.environ.get("GROQ_API_KEY"), audio_file_path=audio_filepath, stt_model="whisper-large-v3")



    #Handle the image input
    if image_filepath:
        doctor_response = analyze_image_with_query(query=system_prompts + speech_to_text_output,encoded_image=encode_image(image_filepath),model = "meta-llama/llama-4-scout-17b-16e-instruct")
    else:
        doctor_response= "No image provided for me to analyze"

    voice_of_doctor = text_to_speech_with_elevenlabs(input_text=doctor_response,output_filepath_mp3="final.mp3")

    return speech_to_text_output, doctor_response, "final.mp3"



#create the interface
iface = gr.Interface(
    fn = process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath"),
        gr.Image(type="filepath")
    ],
    outputs=[
        gr.Textbox(label="Speech to Text"),
        gr.Textbox(label="Doctor's Response"),
       gr.Audio("final.mp3")

    ],
    title="AI Doctor with Vision and Voice"
)

iface.launch(debug=True)