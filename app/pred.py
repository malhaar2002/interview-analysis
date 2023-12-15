import pickle
from speech_to_text import transcribe_video_file
from lexical_extraction import extract_lexical_features
from praat_extraction import extract_praat_features
from emotion import get_emotions


model = pickle.load(open('../models/model_custom.pkl', 'rb'))

# transcript = transcribe_video_file("/home/malhaar/Downloads/rishit.mp4")
transcript = """Hi, my name is Rishi Gupta. I am a third year computer engineering major studying at Cal Poly. I aspire to be a frontend web developer specializing in react and svelte. I was the secretary of my school's tech club node in the 11th grade. Now, in our school, it's supposed to be that there are two 11th grade secretaries and two 12th grade presidents. However, during our tenure, there were no twelve presidents to guide us, so we had to manage the entire club and its functionality by ourselves. So me and my co secretary, we had to organize events, organize teams to compete in inter school tournaments and assist the school in any function and any event they plan and essentially just handle the tech side of things. So that experience taught me a lot of how to manage people, what to say, in what situations, how to be the intermediate between students and teachers, and in any position of authority. So I think it was a transformative experience for me and I will always rely on those lessons that I learned. Recently I was working as a UX developer intern at DBS Bank. I was working in a relatively small team which mainly functioned for the design language system, so my interaction was mostly with my fellow developers and designers. We ran into a roadblock when I was supposed to design the demo for one of the flows, but the deadline was pushed up severely because of a quarterly review. So we had to work around the clock and communicate with designers efficiently to get the job done. It involved me going up to people I'd never met before, I'd never spoken to before, and communicating with them and trying to handle the task at hand. My one weakness is time management. I tend to work late into the night and anyone who works with me has some unusual reactions to that. However, I have been working on it and whenever I'm in a supportive and collaborative team, I tend to align my schedule with theirs so that I am always on call and I'm always effective. To put it simply, I am an incredibly motivated person and I am eager to learn. I just want to overcome any obstacle this opportunity throws my way because I want to learn to overcome those obstacles in the future and I just want to contribute in a workflow as part of a team and adapt to that environment. I want to be a team player."""
lexical_features_dict = extract_lexical_features(transcript)

prosodic_features_dict = extract_praat_features("audio.wav")
print(prosodic_features_dict)

emotions_dict = get_emotions("rishit.mp4")
print(emotions_dict)

