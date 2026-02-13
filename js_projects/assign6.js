var mapArr;
var filArr;
function multiplyByTen(myArray){
    mapArr=myArray.map((e)=>{return e*10;});
    return mapArr;
}
function filterArray(myArray){
    filArr=myArray.filter((e)=>{return e%2==0;});
    return filArr;
}
const input1=[12, 2, 2, 4, 1];
const input2 = [12, 5, 7, 8, 3, 2];
output=multiplyByTen(input1);
output1=filterArray(input2);
console.log("Input: ",input1);
console.log("Output: ",output);
console.log("Filter Input: ",input2);
console.log("Filtered Output: ",output1);
