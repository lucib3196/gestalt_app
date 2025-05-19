import markdown
import pypandoc


def md_to_pdf(input_md, output_pdf):
    pypandoc.convert_file(
        source_file=input_md,
        to="pdf",
        outputfile=output_pdf,
        extra_args=["--pdf-engine=xelatex"],
    )


def md_to_html(input_md, output_html):
    html = pypandoc.convert_file(
        source_file=input_md,
        to="html",
        outputfile=output_html,
    )


# Example
md_to_pdf(
    r"backend/ai_workspace\lecture_processor\v2\final_lecture.md",
    r"backend/ai_workspace\lecture_processor\v2\notes.pdf",
)
md_to_html(
    r"backend/ai_workspace\lecture_processor\v2\final_lecture.md",
    r"backend/ai_workspace\lecture_processor\v2\notes.html",
)
