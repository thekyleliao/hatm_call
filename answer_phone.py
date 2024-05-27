from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather
import random

app = Flask(__name__)

story_dict = {
    1: "https://timberwolf-cheetah-1758.twil.io/assets/story1.mp3",
    2: "https://timberwolf-cheetah-1758.twil.io/assets/story2.mp3",
    3: "https://timberwolf-cheetah-1758.twil.io/assets/story3.mp3",
    4: "https://timberwolf-cheetah-1758.twil.io/assets/story4.mp3",
    5: "https://timberwolf-cheetah-1758.twil.io/assets/story5.mp3"
}

@app.route("/answer", methods=['GET', 'POST'])
def answer_call():
    """Respond to incoming phone calls with a brief message."""
    # Start our TwiML response
    resp = VoiceResponse()

    if 'Digits' in request.values:
        # Get which digit the caller chose
        choice = request.values['Digits']

        # <Say> a different message depending on the caller's choice
        if choice == '1':
            resp.say('Finding you the perfect hacker advice!', voice='Polly.Salli')
            resp.redirect('/story')
            return str(resp)
        elif choice == '2':
            resp.say('Please leave your hacker advice after the beep.', voice='Polly.Salli')
            resp.redirect('/record')
            return str(resp)
        else:
            # If the caller didn't choose 1 or 2, apologize and ask them again
            resp.say("Sorry, I don't understand that choice.", voice='Polly.Salli')

    # Read a message aloud to the caller
    gather = Gather(num_digits=1)
    resp.say("Welcome to Hack at the Museum! This is an experiential art piece. For a piece of hacker advice, press 1. To send in your advice, press 2.", voice='Polly.Salli')
    resp.append(gather)

    resp.redirect('/answer')

    return str(resp)

@app.route("/record", methods=['GET', 'POST'])
def record():
    """Returns TwiML which prompts the caller to record a message"""
    # Start our TwiML response
    response = VoiceResponse()

    # Use <Record> to record the caller's message
    response.record()

    # End the call with <Hangup>
    response.hangup()

    return str(response)

@app.route("/story", methods=['GET', 'POST'])
def story():
    """Returns TwiML which reads a story to the caller"""
    # Start our TwiML response
    response = VoiceResponse()

    # Read a story to the caller
    response.say("Hackers do a lot of cool things! Here's advice for you.", voice='Polly.Salli')
    response.play(story_dict[random.randint(1,5)])

    # End the call with <Hangup>
    response.hangup()

    return str(response)

if __name__ == "__main__":
    app.run(debug=True)
