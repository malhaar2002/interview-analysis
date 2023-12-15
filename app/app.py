import streamlit as st
import numpy as np

# Function to perform video analysis and return predicted labels
def video_analysis(uploaded_file):
    # Placeholder for analysis logic - replace this with your actual analysis code
    # For demonstration purposes, generating random labels
    labels = generate_sample_labels()

    return labels

# Function to display analysis results and provide feedback
def display_results(labels):
    # Display labels where the user performed well and areas to improve side by side
    col1, col2 = st.columns(2)

    # Display labels where the user performed well
    with col1:
        st.subheader("Areas where you shine")
        good_performance = [label for label, score in labels.items() if score == 1]
        for label in good_performance:
            st.markdown(f'- {label}')

    # Display labels where the user has a scope to improve
    with col2:
        st.subheader("Areas to improve")
        improvement_opportunity = [label for label, score in labels.items() if score == 0]
        for label in improvement_opportunity:
            st.markdown(f'- {label}')

    st.write("---")

    # Provide description and tips for each label
    st.subheader("Here's a few tips on how you can improve in each category:")
    for label in labels.keys():
        tips = get_tips(label)
        st.write(f"**{label}:**")
        for tip in tips:
            st.markdown(f'- {tip}')
        st.write("---")


# Function to get label description and tips
def get_tips(label):
    tips = {
        "Engaged": [
            "Maintain eye contact with the camera to convey attentiveness and interest.",
            "Use positive body language to express enthusiasm and engagement.",
            "Ask thoughtful questions and actively listen to the interviewer's prompts."
        ],

        "EyeContact": [
            "Focus on looking directly into the camera for a virtual interview.",
            "Avoid excessive staring at notes or distractions in the room.",
            "Practice a balance between maintaining eye contact and natural blinking."
        ],

        "Smiled": [
            "Smile naturally and periodically throughout the interview.",
            "Practice a friendly and approachable facial expression.",
            "Be mindful of not appearing overly serious or expressionless."
        ],

        "Excited": [
            "Express genuine enthusiasm and excitement about the opportunity.",
            "Use positive and energetic language to convey your interest in the role.",
            "Share specific reasons why you are excited about the prospect of joining the company."
        ],

        "SpeakingRate": [
            "Speak at a moderate pace to ensure clarity and comprehension.",
            "Practice using pauses strategically to emphasize key points.",
            "Avoid speaking too rapidly, which can be challenging for the interviewer to follow."
        ],

        "NoFillers": [
            "Minimize the use of filler words such as 'um,' 'uh,' or 'like.'",
            "Practice pausing instead of using fillers to gather thoughts.",
            "Consciously focus on speaking with clarity and precision."
        ],

        "Friendly": [
            "Project a warm and approachable tone throughout the conversation.",
            "Use positive language and expressions to convey friendliness.",
            "Express genuine interest in the role and the company."
        ],

        "Paused": [
            "Use strategic pauses to allow the interviewer to process information.",
            "Avoid rushing through responses; take your time to formulate answers.",
            "Pausing can convey thoughtfulness and professionalism."
        ],

        "EngagingTone": [
            "Vary your tone to add emphasis and interest to your responses.",
            "Avoid a monotonous voice by incorporating changes in pitch and intonation.",
            "Practice conveying enthusiasm and passion through your tone."
        ],

        "StructuredAnswers": [
            "Organize your responses with a clear introduction, body, and conclusion.",
            "Use examples and anecdotes to illustrate your points.",
            "Practice concise and focused answers to showcase your communication skills."
        ],

        "Calm": [
            "Practice mindfulness techniques to stay calm and composed.",
            "Breathe deeply to manage nervousness and stress.",
            "Remember that it's okay to take a moment to collect your thoughts."
        ],

        "NotStressed": [
            "Prioritize self-care before the interview to reduce stress levels.",
            "Prepare thoroughly to build confidence in your knowledge and abilities.",
            "Focus on the present moment and the opportunity to showcase your skills."
        ],

        "Focused": [
            "Demonstrate active listening by fully engaging with the interviewer's questions.",
            "Maintain a clear and concise focus on relevant details in your responses.",
            "Avoid distractions and stay present throughout the interview."
        ],

        "NotAwkward": [
            "Practice common interview scenarios to build confidence.",
            "Maintain professional and confident body language.",
            "Remember that it's okay to acknowledge nerves and redirect them into positive energy."
        ]
    }

    return tips.get(label, "")

# Main function to run the Streamlit app
def main():
    st.title("Interview Analyzer")

    # Upload Video
    uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "avi"])

    if uploaded_file is not None:
        # Display uploaded video
        st.video(uploaded_file)

        # Perform analysis
        analysis_button = st.button("Perform Analysis")
        if analysis_button:
            labels = video_analysis(uploaded_file)
            display_results(labels)

if __name__ == "__main__":
    main()
