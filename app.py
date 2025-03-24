import streamlit as st
from src.gen_resume import get_resume, md_to_pdf

def main():
    st.set_page_config(page_title="Resume Generator")

    st.markdown("""
        <style>
            .stButton {
                display: flex;
                justify-content: center;
                align-items: center;
                width: 100%;
            }
            .stButton button {
                display: inline-block;
                margin: auto;
            }
        </style>
    """, unsafe_allow_html=True)

    st.title("Resume Generator")    

    # Initialize session state variables if they don't exist
    if 'resume' not in st.session_state:
        st.session_state.resume = None
    if 'generated' not in st.session_state:
        st.session_state.generated = False

    col1, col2 = st.columns(2)

    with col1:
        st.session_state.candidate_name = st.text_area("Candidate Name", height=70)
        st.session_state.education_details = st.text_area("Education Details", height=70)
        st.session_state.job_experience = st.text_area("Job Experience", height=70)
        st.session_state.skills = st.text_area("Skills", height=70)
        st.session_state.projects = st.text_area("Projects", height=70)
        st.session_state.contact_details = st.text_area("Contact Details", height=70)

    with col2:
        st.session_state.job_description = st.text_area("Job Description", height=530)

    # Ensure all fields are filled
    all_fields_filled = (
        st.session_state.candidate_name.strip() != "" and
        st.session_state.education_details.strip() != "" and
        st.session_state.job_experience.strip() != "" and
        st.session_state.skills.strip() != "" and
        st.session_state.job_description.strip() != "" and
        st.session_state.contact_details.strip() != "" and
        st.session_state.projects.strip() != ""
    )

    if all_fields_filled:
        if st.button("Generate Resume"):
            # Clear any previous resume data before generating new one
            st.session_state.resume = None
            st.session_state.generated = False

            # Generate new resume
            candidate_details = f"""
                Name: {st.session_state.candidate_name}
                Education Details: {st.session_state.education_details}
                Job Experience: {st.session_state.job_experience}
                Skills: {st.session_state.skills}
                Contact Details: {st.session_state.contact_details}
                Projects: {st.session_state.projects}
            """

            # Generate the resume and store it in session state
            st.session_state.resume = get_resume(candidate_details, st.session_state.job_description)
            st.session_state.generated = True

        # Show generated resume if available
        if st.session_state.generated and st.session_state.resume:
            st.markdown(st.session_state.resume)
            
            # Provide a download button for the resume
            st.download_button(
                label="⬇️ Download Resume",
                data=md_to_pdf(st.session_state.resume),
                file_name=f"{st.session_state.candidate_name} Resume.pdf",
                mime="application/pdf",
            )

    else:
        # Disable the button if fields are not filled
        st.button("Generate Resume", disabled=True)

if __name__ == "__main__":
    main()
