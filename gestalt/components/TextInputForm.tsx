export default function TextInputForm() {
  return (
    <form>
      <div className="form-floating">
        <textarea
          className="form-control"
          placeholder="Leave a comment here"
          id="floatingTextarea"
        ></textarea>
        <label className="floatingTextarea">Comments</label>
      </div>
    </form>
  );
}
