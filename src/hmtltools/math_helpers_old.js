const math = require('mathjs')


function removeItemOnce(arr, value) {
    var index = arr.indexOf(value);
    if (index > -1) {
      arr.splice(index, 1);
    }
    return arr;
  }

function getRandomPermutationArray(A1) {
    A = A1._data;
    numEls = A.length;
    B = [];
 for (let i = 0; i < numEls; i++) {
    x = math.pickRandom(A);
    y = removeItemOnce(A,x);
    B.push(x);
 }
 return B;
}

function getRandomPermutationRange(num){
    A = math.range(0, num);
    B = getRandomPermutationArray(A);
    return B;

}

function getRandomInt(max) {
  return Math.floor(Math.random() * max);
}

module.exports = {
    getRandomPermutationRange,
    getRandomInt
}

// B = getRandomPermutationRange(4);
// console.log(B);