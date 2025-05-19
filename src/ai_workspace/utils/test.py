from .helper import pdf_to_image_persistent
import os
import asyncio

async def main():
    base_path = os.path.dirname(os.path.abspath(__file__))
    pdf_path = r"C:\Users\lberm\OneDrive\Documents\Github\gestalt_app\Lectures\Lec11-post.pdf"
    pdf_directory = os.path.dirname(pdf_path)
    output_dir = os.path.join(pdf_directory, "lecture_images")
    os.makedirs(output_dir, exist_ok=True)

    image_paths = await pdf_to_image_persistent(pdf_path, output_dir,annotate=True)

if __name__ =="__main__":
    asyncio.run(main())
    