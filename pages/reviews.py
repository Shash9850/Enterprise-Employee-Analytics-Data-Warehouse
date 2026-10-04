import streamlit as st
from datetime import date

from managers.review_manager import ReviewManager
from managers.employee_manager import EmployeeManager
from managers.project_manager import ProjectManager
from models.review import Review


st.set_page_config(
    page_title="Performance Reviews",
    page_icon="📝",
    layout="wide"
)


review_manager = ReviewManager()
employee_manager = EmployeeManager()
project_manager = ProjectManager()


st.title("📝 Performance Reviews")
st.caption("Create, view, update, and delete employee performance reviews.")


# ---------------------------------------------------------
# Helper functions
# ---------------------------------------------------------

def employee_exists(employee_id):
    """Check whether an employee exists in the OLTP database."""
    return employee_manager.get_employee(employee_id) is not None


def project_exists(project_id):
    """Check whether a project exists in the OLTP database."""
    return project_manager.get_project(project_id) is not None


# ---------------------------------------------------------
# Submit Performance Review
# ---------------------------------------------------------

st.header("Submit Performance Review")

with st.form("create_review_form"):

    col1, col2 = st.columns(2)

    with col1:
        employee_id = st.text_input(
            "Employee ID *",
            placeholder="Example: E000001"
        )

        project_id_input = st.text_input(
            "Project ID",
            placeholder="Optional"
        )

        review_date = st.date_input(
            "Review Date *",
            value=date.today()
        )

    with col2:
        performance_rating = st.selectbox(
            "Performance Rating *",
            options=[1, 2, 3, 4, 5],
            index=2
        )

        reviewer_name = st.text_input(
            "Reviewer Name *",
            placeholder="Example: Amogh"
        )

        comments = st.text_area(
            "Comments",
            placeholder="Enter review comments..."
        )

    submit_review = st.form_submit_button(
        "Submit Review",
        type="primary"
    )


if submit_review:

    employee_id = employee_id.strip()

    if not employee_id:
        st.error("Employee ID is required.")

    elif not employee_exists(employee_id):
        st.error(f"Employee {employee_id} does not exist.")

    elif not reviewer_name.strip():
        st.error("Reviewer name is required.")

    else:
        # Project ID is optional because reviews.project_id allows NULL.
        project_id = None

        if project_id_input.strip():

            try:
                project_id = int(project_id_input.strip())

                if not project_exists(project_id):
                    st.error(f"Project {project_id} does not exist.")
                    project_id = None

            except ValueError:
                st.error("Project ID must be a valid integer.")
                project_id = None

        # Only create when the project input is valid.
        if not project_id_input.strip() or project_id is not None:

            review = Review(
                review_id=None,
                employee_id=employee_id,
                project_id=project_id,
                review_date=review_date,
                performance_rating=performance_rating,
                reviewer_name=reviewer_name.strip(),
                comments=comments.strip()
            )

            success = review_manager.create_review(review)

            if success:
                st.success(
                    f"Review submitted successfully. "
                    f"Generated Review ID: {review.review_id}"
                )
            else:
                st.error("Review could not be created.")


st.divider()


# ---------------------------------------------------------
# Find Review
# ---------------------------------------------------------

st.header("Find Review")

search_col1, search_col2 = st.columns([2, 1])

with search_col1:
    search_review_id = st.number_input(
        "Review ID",
        min_value=1,
        step=1,
        value=None,
        placeholder="Enter Review ID"
    )

with search_col2:
    search_review = st.button("Search Review")


if search_review:

    if search_review_id is None:
        st.warning("Enter a Review ID.")

    else:
        review = review_manager.get_review(int(search_review_id))

        if review is None:
            st.warning(f"Review {int(search_review_id)} was not found.")

        else:
            st.success("Review found.")

            result_data = {
                "Review ID": review.review_id,
                "Employee ID": review.employee_id,
                "Project ID": review.project_id,
                "Review Date": review.review_date,
                "Performance Rating": review.performance_rating,
                "Reviewer": review.reviewer_name,
                "Comments": review.comments
            }

            st.json(result_data)


st.divider()


# ---------------------------------------------------------
# Update Review
# ---------------------------------------------------------

st.header("Update Review")

update_id = st.number_input(
    "Review ID to Update",
    min_value=1,
    step=1,
    value=None,
    placeholder="Enter Review ID"
)

load_review = st.button("Load Review")


if load_review:

    if update_id is None:
        st.warning("Enter a Review ID.")

    else:
        review = review_manager.get_review(int(update_id))

        if review is None:
            st.warning(f"Review {int(update_id)} was not found.")
            st.session_state.pop("review_to_update", None)

        else:
            st.session_state["review_to_update"] = review
            st.success("Review loaded. You can now edit it.")


if "review_to_update" in st.session_state:

    review = st.session_state["review_to_update"]

    with st.form("update_review_form"):

        st.text_input(
            "Review ID",
            value=str(review.review_id),
            disabled=True
        )

        employee_id = st.text_input(
            "Employee ID",
            value=review.employee_id
        )

        project_id_input = st.text_input(
            "Project ID",
            value="" if review.project_id is None else str(review.project_id)
        )

        review_date = st.date_input(
            "Review Date",
            value=review.review_date
        )

        performance_rating = st.selectbox(
            "Performance Rating",
            options=[1, 2, 3, 4, 5],
            index=review.performance_rating - 1
        )

        reviewer_name = st.text_input(
            "Reviewer Name",
            value=review.reviewer_name or ""
        )

        comments = st.text_area(
            "Comments",
            value=review.comments or ""
        )

        update_review = st.form_submit_button(
            "Save Changes",
            type="primary"
        )

    if update_review:

        employee_id = employee_id.strip()

        if not employee_id:
            st.error("Employee ID is required.")

        elif not employee_exists(employee_id):
            st.error(f"Employee {employee_id} does not exist.")

        elif not reviewer_name.strip():
            st.error("Reviewer name is required.")

        else:

            project_id = None
            project_valid = True

            if project_id_input.strip():

                try:
                    project_id = int(project_id_input.strip())

                    if not project_exists(project_id):
                        st.error(f"Project {project_id} does not exist.")
                        project_valid = False

                except ValueError:
                    st.error("Project ID must be a valid integer.")
                    project_valid = False

            if project_valid:

                updated_review = Review(
                    review_id=review.review_id,
                    employee_id=employee_id,
                    project_id=project_id,
                    review_date=review_date,
                    performance_rating=performance_rating,
                    reviewer_name=reviewer_name.strip(),
                    comments=comments.strip()
                )

                success = review_manager.update_review(updated_review)

                if success:
                    st.success(
                        f"Review {review.review_id} updated successfully."
                    )
                    st.session_state.pop("review_to_update", None)

                else:
                    st.error("Review could not be updated.")


st.divider()


# ---------------------------------------------------------
# Delete Review
# ---------------------------------------------------------

st.header("Delete Review")

delete_id = st.number_input(
    "Review ID to Delete",
    min_value=1,
    step=1,
    value=None,
    placeholder="Enter Review ID"
)

delete_review = st.button(
    "Delete Review",
    type="secondary"
)


if delete_review:

    if delete_id is None:
        st.warning("Enter a Review ID.")

    else:

        review = review_manager.get_review(int(delete_id))

        if review is None:
            st.warning(f"Review {int(delete_id)} was not found.")

        else:

            success = review_manager.delete_review(int(delete_id))

            if success:
                st.success(
                    f"Review {int(delete_id)} deleted successfully."
                )

            else:
                st.error("Review could not be deleted.")


st.divider()


# ---------------------------------------------------------
# View Reviews
# ---------------------------------------------------------

st.header("View Reviews")

st.caption(
    "The database contains a large synthetic review dataset. "
    "Use a specific Review ID above when working with individual records."
)

if st.button("Load Sample Reviews"):

    reviews = review_manager.get_all_reviews()

    if not reviews:
        st.info("No reviews found.")

    else:

        # Display only a small sample in the UI.
        sample_reviews = reviews[:100]

        review_data = []

        for review in sample_reviews:
            review_data.append({
                "Review ID": review.review_id,
                "Employee ID": review.employee_id,
                "Project ID": review.project_id,
                "Review Date": review.review_date,
                "Rating": review.performance_rating,
                "Reviewer": review.reviewer_name,
                "Comments": review.comments
            })

        st.dataframe(
            review_data,
            width="stretch",
            hide_index=True
        )

        st.caption(
            f"Showing first {len(sample_reviews)} reviews "
            f"out of {len(reviews):,} total reviews."
        )