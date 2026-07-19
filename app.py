#Part-1
import streamlit as st

from src.generator import compile_quiz_data
from src.database import setup_and_populate_db


# PAGE CONFIG

st.set_page_config(
    page_title="AI-Powered Sports Quiz Generation Agent",
    
    layout="wide"
)

# DATABASE
 
@st.cache_resource
def prepare_database():
    setup_and_populate_db()

prepare_database()
 
# SESSION STATE 

DEFAULTS = {

    "quiz": None,

    "context": "",

    "submitted": False,

    "score": 0,

    "sport": "Cricket",

    "difficulty": "Easy",

    "page": "Quiz",

    "history": [],

    "current_answers": []

}

for key, value in DEFAULTS.items():

    if key not in st.session_state:

        st.session_state[key] = value

 
# HELPER FLAGS
 

quiz_active = (

    st.session_state.quiz is not None

    and

    not st.session_state.submitted

)

 
# HEADER
 

st.title("AI-Powered Sports Quiz Generation Agent")


st.divider()

 
# SIDEBAR
 

st.sidebar.header("Quiz Settings")

SPORTS = [

    "Cricket",

    "Football",

    "Basketball",

    "Badminton",

    "Tennis"

]

LEVELS = [

    "Easy",

    "Medium",

    "Hard"

]

sport = st.sidebar.selectbox(

    "Sport",

    SPORTS,

    index=SPORTS.index(
        st.session_state.sport
    ),

    disabled=quiz_active

)

difficulty = st.sidebar.selectbox(

    "Difficulty",

    LEVELS,

    index=LEVELS.index(
        st.session_state.difficulty
    ),

    disabled=quiz_active

)

st.sidebar.write("")

 
# GENERATE QUIZ
 

generate = st.sidebar.button(

    "Generate Quiz",

    disabled=quiz_active

)

if generate:

    with st.spinner(
        "Generating quiz..."
    ):

        quiz, context = compile_quiz_data(

            sport,

            difficulty

        )

    st.session_state.quiz = quiz

    st.session_state.context = context

    st.session_state.sport = sport

    st.session_state.difficulty = difficulty

    st.session_state.submitted = False

    st.session_state.score = 0

    st.session_state.current_answers = []

    # Clear radio buttons

    for i in range(4):

        key = f"answer_{i}"

        if key in st.session_state:

            del st.session_state[key]

    st.rerun()

 
# NAVIGATION
 

st.sidebar.divider()

st.sidebar.subheader("Navigation")

page = st.sidebar.radio(

    "",

    [

        "Quiz",

        "Performance Dashboard",

        "Retrieved RAG Context"

    ],

    index=[

        "Quiz",

        "Performance Dashboard",

        "Retrieved RAG Context"

    ].index(st.session_state.page)

)

if page != st.session_state.page:

    st.session_state.page = page

    st.rerun()

 
# CURRENT QUIZ
 

st.sidebar.divider()

st.sidebar.subheader("Current Quiz")

st.sidebar.write(

    f"**Sport :** {st.session_state.sport}"

)

st.sidebar.write(

    f"**Difficulty :** {st.session_state.difficulty}"

)

if st.session_state.quiz is None:

    st.sidebar.info("No Quiz Generated")

elif st.session_state.submitted:

    st.sidebar.success(

        f"Completed\n\nScore : {st.session_state.score}/4"

    )

else:

    st.sidebar.warning("Quiz In Progress")

#Part-2
     
# QUIZ PAGE
 

if st.session_state.page == "Quiz":

    if st.session_state.quiz is None:

        st.info(
            "Select a sport and difficulty from the sidebar and click Generate Quiz."
        )

        st.stop()

    st.subheader(
        f"{st.session_state.sport} Quiz ({st.session_state.difficulty})"
    )

    if st.session_state.submitted:

        st.success(
            f" Score : {st.session_state.score} / {len(st.session_state.quiz)}"
        )

    st.write("")

     
    # QUESTION GRID
     

    row1 = st.columns(2, gap="large")
    row2 = st.columns(2, gap="large")

    cards = [

        row1[0],
        row1[1],
        row2[0],
        row2[1]

    ]

    for i, q in enumerate(st.session_state.quiz):

        with cards[i]:

            with st.container(border=True):

                st.markdown(
                    f"### Question {i+1}"
                )

                st.write(
                    q["question"]
                )

                options = [

                    f"A. {q['options']['A']}",

                    f"B. {q['options']['B']}",

                    f"C. {q['options']['C']}",

                    f"D. {q['options']['D']}"

                ]

                answer = st.radio(

                    "Choose Answer",

                    options,

                    key=f"answer_{i}",

                    disabled=st.session_state.submitted

                )

                  
                # Show Result
                  

                if st.session_state.submitted:

                    selected = answer[0]

                    correct = q["correct_answer"]

                    if selected == correct:

                        st.success("Correct")

                    else:

                        st.error("Incorrect")

                    st.write(
                        f"**Your Answer :** {selected}"
                    )

                    st.write(
                        f"**Correct Answer :** {correct}"
                    )

                    st.info(
                        q["explanation"]
                    )

    st.write("")
    st.write("")

     
    # BUTTONS
     

    left, middle, right = st.columns([4,2,4])

    with middle:

        
        # SUBMIT QUIZ

        if not st.session_state.submitted:

            if st.button("Submit Quiz"):

                score = 0

                answers = []

                for i, q in enumerate(

                    st.session_state.quiz

                ):

                    selected = st.session_state[
                        f"answer_{i}"
                    ][0]

                    answers.append(selected)

                    if selected == q["correct_answer"]:

                        score += 1

                st.session_state.score = score

                st.session_state.submitted = True

                st.session_state.current_answers = answers

                 
                # Dashboard updates immediately
                 

                st.session_state.history.append(

                    {

                        "sport":
                        st.session_state.sport,

                        "difficulty":
                        st.session_state.difficulty,

                        "score":
                        score,

                        "quiz":
                        st.session_state.quiz,

                        "answers":
                        answers

                    }

                )

                st.rerun()

          
        # GENERATE NEW QUIZ
          

        else:

            if st.button("Generate New Quiz"):

                with st.spinner(
                    "Generating New Quiz..."
                ):

                    quiz, context = compile_quiz_data(

                        st.session_state.sport,

                        st.session_state.difficulty

                    )

                st.session_state.quiz = quiz

                st.session_state.context = context

                st.session_state.submitted = False

                st.session_state.score = 0

                st.session_state.current_answers = []

                # Remove previous radio selections

                for i in range(4):

                    key = f"answer_{i}"

                    if key in st.session_state:

                        del st.session_state[key]

                st.rerun()

#Part3
 
# PERFORMANCE DASHBOARD
 

elif st.session_state.page == "Performance Dashboard":

    st.header("Performance Dashboard")

    if len(st.session_state.history) == 0:

        st.info(
            "Complete a quiz to view your performance."
        )

    else:

        history = st.session_state.history

        current_score = history[-1]["score"]

        previous_score = (

            history[-2]["score"]

            if len(history) > 1

            else 0

        )

        best_score = max(

            item["score"]

            for item in history

        )

        average_score = (

            sum(

                item["score"]

                for item in history

            )

            /

            len(history)

        )

        improvement = (

            current_score

            -

            previous_score

        )

         
        # METRICS
         

        c1, c2, c3, c4, c5 = st.columns(5)

        c1.metric(

            "Current",

            f"{current_score}/4"

        )

        c2.metric(

            "Previous",

            f"{previous_score}/4"

        )

        c3.metric(

            "Average",

            f"{average_score:.2f}/4"

        )

        c4.metric(

            "Best",

            f"{best_score}/4"

        )

        c5.metric(

            "Improvement",

            f"{improvement:+}"

        )

        st.divider()

        st.subheader("📚 Quiz History")

         
        # HISTORY
         

        for attempt, quiz_data in enumerate(

            reversed(history),

            start=1

        ):

            with st.expander(

                f"Attempt {len(history)-attempt+1}"

                f" | "

                f"{quiz_data['sport']}"

                f" | "

                f"{quiz_data['difficulty']}"

                f" | "

                f"Score {quiz_data['score']}/4"

            ):

                for i, q in enumerate(

                    quiz_data["quiz"]

                ):

                    with st.container(border=True):

                        st.markdown(

                            f"### Question {i+1}"

                        )

                        st.write(

                            q["question"]

                        )

                        st.write(

                            f"**Your Answer:** "

                            f"{quiz_data['answers'][i]}"

                        )

                        st.write(

                            f"**Correct Answer:** "

                            f"{q['correct_answer']}"

                        )

                        if (

                            quiz_data["answers"][i]

                            ==

                            q["correct_answer"]

                        ):

                            st.success(

                                "Correct"

                            )

                        else:

                            st.error(

                                "Incorrect"

                            )

                        st.info(

                            q["explanation"]

                        )                

#Part-4
 
# RAG CONTEXT PAGE
 

elif st.session_state.page == "Retrieved RAG Context":

    st.header("🔍 Retrieved RAG Context")

    if st.session_state.context == "":

        st.info(
            "Generate a quiz first to view the retrieved context."
        )

    else:

        st.write(
            """
The following information was retrieved before the quiz
was generated.

This includes:

• Historical sports facts from ChromaDB

• Latest sports news from DuckDuckGo Search

Gemini used this information while creating the quiz.
"""
        )

        st.code(

            st.session_state.context,

            language="text"

        )

        st.download_button(

            label="Download Context",

            data=st.session_state.context,

            file_name="rag_context.txt",

            mime="text/plain"

        )

 
# FOOTER
 

st.divider()

left, middle, right = st.columns([1,2,1])

