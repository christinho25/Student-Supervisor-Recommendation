import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

# Actual data for supervisors' research interests
supervisors = {
    'Dr. Bassey O. Orie': ['differential equations', 'partial differential equations', 'q-partial differential equations', 'Numerical Methods', 'functional analysis'],
    'Dr. Barth A. Uchendu': ['time series', 'operations research', 'sampling', 'data analysis'],
    'Dr. Charles N. Eke': ['econometrics', 'operations research', 'regression'],
    'Dr. Jude Ajaraogu ': ['sampling', 'design', 'data analysis', 'probability'],
    'Dr. Desmond Onuoha ': ['design', 'time series', 'sampling', 'regression'],
    'Dr. Dozie Felix Nwosu ': ['sampling', 'design', 'data analysis'],
    'Dr. Ifeoma Chukwunezu ': ['algebra', 'modeling', 'differential equations'],
    'Dr. Prisca Duruojinkeya ': ['financial mathematics', 'stochastic process', 'differential equations'],
    'Dr. Philip Uzoma ': ['financial mathematics', 'algebra', 'functional analysis'],
    # Add more supervisors as needed
}

# Constraints
max_students_per_supervisor = 3

# Title and description
st.title("Federal Polytechnic Nekede Owerri")
st.header("Department of Mathematics and Statistics")
st.subheader("Supervisor Recommendation Application System")

st.write("Find the best supervisor based on your research interests.")

# Sidebar for input
st.sidebar.header("Input your research interests")
student_interests_input = st.sidebar.text_input("Enter your research interests (comma-separated):")

# Button to submit input
if st.sidebar.button("Find Supervisor"):
    if student_interests_input:
        # Process the input
        student_interests = [interest.strip().lower() for interest in student_interests_input.split(',')]

        # Vectorizing the data
        all_interests = set(
            [interest for interests in supervisors.values() for interest in interests] + student_interests)
        interest_to_index = {interest: index for index, interest in enumerate(all_interests)}


        def create_vector(interests):
            vector = [1 if interest in interests else 0 for interest in all_interests]
            return np.array(vector)


        supervisors_vectors = {name: create_vector([i.lower() for i in interests]) for name, interests in
                               supervisors.items()}
        student_vector = create_vector(student_interests)

        # Calculate cosine similarity between student and each supervisor
        allocation = {}
        for supervisor_name, supervisor_vector in supervisors_vectors.items():
            similarity = cosine_similarity([student_vector], [supervisor_vector])[0][0]
            st.write(f"Similarity with {supervisor_name}: {similarity}")
            if similarity > 0.5:  # Example threshold, adjust as needed
                # Check if supervisor has reached maximum number of students
                if len(allocation.get(supervisor_name, [])) < max_students_per_supervisor:
                    allocation.setdefault(supervisor_name, []).append((similarity, student_interests))

        # Sort students based on similarity
        for supervisor_name, students in allocation.items():
            allocation[supervisor_name] = sorted(students, key=lambda x: x[0], reverse=True)

        # Display results
        if allocation:
            st.subheader("Recommended Supervisor(s) Based on Similarity:")
            for supervisor, students in allocation.items():
                st.write(f"### {supervisor}:")
                for similarity, interests in students:
                    st.write(f"- **Similarity**: {similarity:.2f}, **Interests**: {', '.join(interests)}")
        else:
            st.write("No suitable supervisor found based on provided interests.")
    else:
        st.write("Please enter your research interests.")