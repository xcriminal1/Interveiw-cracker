import PySimpleGUI as sg
from src import recorder, transcriber, responder

def run_gui():
    sg.theme('DarkBlue3')
    layout = [
        [sg.Text("Hack Interview", font=("Helvetica", 16))],
        [sg.Multiline(key='-TRANSCRIPT-', size=(60, 5), disabled=True)],
        [sg.Multiline(key='-ANSWER-', size=(60, 5), disabled=True)],
        [sg.Button("Record", key='-RECORD-'), sg.Button("Process", key='-PROCESS-'), sg.Exit()]
    ]

    window = sg.Window("Hack Interview", layout)

    audio_file = None
    transcript = ""
    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, 'Exit'):
            break
        elif event == '-RECORD-':
            try:
                audio_file = recorder.record_audio(duration=5)
                sg.popup("Recording complete!")
            except Exception as e:
                sg.popup_error(f"Recording failed: {e}")
        elif event == '-PROCESS-':
            if not audio_file:
                sg.popup_error("Please record audio first!")
                continue
            try:
                transcript = transcriber.transcribe(audio_file)
                window['-TRANSCRIPT-'].update(transcript)
                answer = responder.generate_response(transcript)
                window['-ANSWER-'].update(answer)
            except Exception as e:
                sg.popup_error(f"Processing failed: {e}")

    window.close()
