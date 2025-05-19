const { i } = require("mathjs");
const mathhelper = require("./math_helpers_old.js");

const replace_params = (x, data) => {
  while ((st = x.match("{{"))) {
    stind = st.index;
    enind = x.match("}}").index;
    fullString = x.slice(stind, enind + 2);
    console.log(`FullString is ${fullString}`);
    if (fullString.includes("params")) {
      y = x.slice(stind + 9, enind);
      console.log(`In PARAMS ${y}`);
      d = data["params"][y];
      x = x.replace(fullString, d);
    } else if (fullString.includes("param_labels")) {
      console.log(`In PARAM LABELS ${y}`);
      y = x.slice(stind + 15, enind);
      d = data["param_labels"][y];
      x = x.replace(fullString, d);
    } else if (fullString.includes("correct_answers_labels")) {
      console.log(`In CORRECT ANSWER LABEL ${y}`);
      y = x.slice(stind + 25, enind);
      d = data["correct_answers_labels"][y];
      x = x.replace(fullString, d);
    }
    //       console.log(`From ${fullString}, we are replacing ${y} with ${d}`);
  }
  return x;
};

const pl_symbolic_input = ($, qdate, el) => {
  const att = $(el).attr();
  dp = att["answers-name"];
  val = qdata["correct_answers"][dp];
  let label = att["label"];
  if (!label) {
    label = "Answer";
  }
  const formOpen = `<form action = "" method =""> <fieldset class="answers"> <legend> Answer </legend>`;
  let s = `<p> <label for="response"> ${label} </label> <input type="text" name="response" id="C" size="50"/> </p>`;
  let formEnd = "</fieldset> </form>";
  htmlString = formOpen.concat(s);
  htmlString = htmlString.concat(formEnd);
  return htmlString;
};

const pl_figure = ($, qname, el) => {
  const att = $(el).attr();
  nm = att["file-name"];
  //imFileName = qdir + '/clientFilesQuestion/' + nm;
  imFileName = "/questions/" + qname + "/" + nm;
  const htmlString = `<img src="${imFileName}" alt="Picture for problem" width="300" height="300" class="pic" />`;
  return htmlString;
};

const pl_checkbox = ($, el) => {
  const att = $(el).attr();
  nm = att["answers-name"];
  cs = $(el).children();
  // console.log(cs.length);

  let htmlString = `<form class="answers" action="" method="" name = ${nm}>`;
  B = mathhelper.getRandomPermutationRange(cs.length);
  let correctAnswers = [];
  for (let j = 0; j < B.length; j++) {
    let i = B[j];
    //  for (let i = 0; i < cs.length; i++) {
    let tx = cs[i.toString()].children[0].data.trim();
    // console.log(`${i} : ${tx}`);
    let id = "child".concat(i);
    console.log(
      "Child node correctness is ",
      cs[i.toString()]["attribs"]["correct"]
    );
    if (cs[i.toString()]["attribs"]["correct"] === "true") {
      console.log(`Pushing ${id} onto correct-answers`);
      correctAnswers.push(id);
    }
    let s = `<input class ="response" type="checkbox" name="${nm}" id="${id}">  <label> ${tx} </label> <br\>`;
    htmlString = htmlString.concat(s);
  }
  htmlString += "<div class='feedback'> </div>";
  htmlString = htmlString.concat("</form>");
  return {
    name: nm,
    htmlString: htmlString,
    correctAnswers: correctAnswers,
  };
};

const pl_multiple_choice = ($, el) => {
  const att = $(el).attr();
  // console.log('Attribute = ', att);
  nm = att["answers-name"];
  cs = $(el).children();
  let htmlString = `<form name = ${nm} class = "answers" action="" method="">`;
  htmlString += "<fieldset>";
  B = mathhelper.getRandomPermutationRange(cs.length);
  let correctAnswers = [];
  for (let j = 0; j < B.length; j++) {
    let i = B[j];
    //  for (let i = 0; i < cs.length; i++) {
    let tx = cs[i.toString()].children[0].data.trim();
    let id = "child".concat(i);
    console.log(
      "Child node correctness is ",
      cs[i.toString()]["attribs"]["correct"]
    );
    if (cs[i.toString()]["attribs"]["correct"] === "true") {
      console.log(`Pushing ${id} onto correct-answers`);
      correctAnswers.push(id);
    }
    let s = `<input type="radio" name="${nm}" class="response" id="${id}"> ${tx} <br/> `;
    // console.log(`This string is: ${s}`);
    htmlString = htmlString.concat(s);
  }
  htmlString += "</fieldset>";
  htmlString += "<div class='feedback'> </div>";
  htmlString = htmlString.concat("</form>");
  return {
    name: nm,
    htmlString: htmlString,
    correctAnswers: correctAnswers,
  };
};

const pl_number_input_fixed = ($, qdata, el) => {
  const att = $(el).attr();
  let correctAnswers = [];
  dp = att["answers-name"];
  if (att["correct-answer-fixed"]) {
    val = att["correct-answer-fixed"];
    correctAnswers.push(val);
  } else {
    val = qdata["correct_answers"][dp];
  }
  const formOpen = `<form class = "answers" name="${dp}" action = "" method =""> <fieldset class=""> <legend> Answer </legend>`;
  let s = `<p> <label for="response"> ${att["label"]} </label> <input type="text" class="response" name="${dp}" id="${dp}" size="50"/> </p>`;

  let formEnd = "</fieldset> <div class='feedback'> </div> </form>";
  htmlString = formOpen.concat(s);
  htmlString = htmlString.concat(formEnd);

  return {
    name: dp,
    htmlString: htmlString,
    correctAnswers: correctAnswers,
  };
};

const pl_number_input = ($, qdata, el) => {
  const att = $(el).attr();
  dp = att["answers-name"];
  if (att["correct-answer-fixed"]) {
    val = att["correct-answer"];
  } else {
    val = qdata["correct_answers"][dp];
  }
  const formOpen = `<form class = "answers" name="${dp}" action = "" method =""> <fieldset class=""> <legend> Answer </legend>`;
  let s = `<p> <label for="response"> ${att["label"]} </label> <input type="text" class="response" name="${dp}" id="${dp}" size="50"/> </p>`;

  let formEnd = "</fieldset> <div class='feedback'> </div> </form>";
  htmlString = formOpen.concat(s);
  htmlString = htmlString.concat(formEnd);
  return htmlString;
};

const pl_matrix_input = ($, qdata, el) => {
  const att = $(el).attr();
  // console.log('Attribute = ', att);
  // console.log('QDATA-222 ', qdata);
  dp = att["answers-name"];
  //  console.log('ANSWERS NAME is ',dp);
  val = qdata["correct_answers"][dp];
  //  console.log('CORRECT ANSWER IS :',val);
  let st = emitLatexMatrix(val);
  console.log("C = ", st);
  const formOpen = `<form class="answers" name = "${dp}" action = "" method =""> <fieldset > <legend> Answer </legend>`;
  let s = `<p> <label for="response"> ${att["label"]} </label> <input type="text" class="response" name="response" id="C" size="50"/> </p>`;
  let formEnd = "</fieldset> <div class='feedback'> </div> </form>";
  htmlString = formOpen.concat(s);
  htmlString = htmlString.concat(formEnd);
  return htmlString;
  //  console.log(htmlString);
};

const pl_matrix_latex = ($, qdata, el) => {
  const att = $(el).attr();
  console.log(att["params-name"]);
  dp = att["params-name"];
  val = qdata["params"][dp];

  let st = emitLatexMatrix(val);
  return st;
};

const emitLatexMatrix = (mat) => {
  //   console.log('In Emit LATEX: ', mat);
  let innerString = "";
  ms = mat._value;
  //  console.log('in Emit Latex Matrix ', ms);
  let nrow = ms.length;
  let c = 0;
  ms.forEach((row) => {
    let rowString = "";
    let ncol = row.length;
    let r = 0;
    row.forEach((el) => {
      rowString = rowString.concat(el);

      if (r < ncol - 1) {
        rowString = rowString.concat(" & ");
      }
      r += 1;
    });
    innerString = innerString.concat(rowString);

    if (c < nrow - 1) {
      innerString = innerString.concat("\\\\");
    }
    c += 1;
  });

  let st = "\\begin{bmatrix} ".concat(innerString);
  st = st.concat("\\end{bmatrix}");
  return st;
};

module.exports = {
  pl_checkbox,
  pl_multiple_choice,
  pl_figure,
  pl_number_input_fixed,
  pl_number_input,
  pl_symbolic_input,
  pl_checkbox,
  pl_multiple_choice,
  pl_matrix_input,
  pl_matrix_latex,
  replace_params,
};
