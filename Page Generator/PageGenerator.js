import { writeFile } from 'fs';

console.log('test');
let link = "http://orteil.dashnet.org/legacy/data.js";


let mainData = {};
mainData.gameObjects = {};
let G={}; 
G.AddData=function(obj) {
    mainData['data'] = {};
    for (var i in obj) {
		mainData.data[i]=obj[i];
	}
    obj.func();
}
G.props=[];
G.funcs=[];

function shuffle(array) {
    var tmp, current, top = array.length;

    if(top) while(--top) {
        current = Math.floor(Math.random() * (top + 1));
        tmp = array[current];
        array[current] = array[top];
        array[top] = tmp;
    }
    return array;
}

G.Res=function(obj) {
    mainData.gameObjects[obj.name] = obj;
    mainData.gameObjects[obj.name].type = 'res';
}
G.Unit=function(obj) {
    mainData.gameObjects[obj.name] = obj;
    mainData.gameObjects[obj.name].type = 'unit';
}
G.ChooseBox=function(obj) {
    mainData.gameObjects[obj.name] = obj;
    mainData.gameObjects[obj.name].type = 'choosebox';
}
G.Tech=function(obj) {
    mainData.gameObjects[obj.name] = obj;
    mainData.gameObjects[obj.name].type = 'tech';
}
G.Trait=function(obj) {
    mainData.gameObjects[obj.name] = obj;
    mainData.gameObjects[obj.name].type = 'trait';
}
G.Policy=function(obj) {
    mainData.gameObjects[obj.name] = obj;
    mainData.gameObjects[obj.name].type = 'policy';
}
G.Land=function(obj) {
    mainData.gameObjects[obj.name] = obj;
    mainData.gameObjects[obj.name].type = 'land';
}
G.Goods=function(obj) {
    mainData.gameObjects[obj.name] = obj;
    mainData.gameObjects[obj.name].type = 'goods';
}
G.TileEffect=function(obj) {
    mainData.gameObjects[obj.name] = obj;
    mainData.gameObjects[obj.name].type = 'tile effect';
}
G.Achiev=function(obj) {
    mainData.gameObjects[obj.name] = obj;
    mainData.gameObjects[obj.name].type = 'achiev';
}
function choose(arr) {return arr[Math.floor(Math.random()*arr.length)];}

G.unitCategories=[];
G.knowCategories=[];
G.policyCategories=[];
G.legacyBonuses=[];
G.contextNames=[];

async function getMod() {
    const response = await fetch(link);
    const text = await response.text();
    return text;
}

async function testMod() {
    let modtext = await getMod();
    eval(modtext);
    console.log(JSON.stringify(mainData, null, 4));
    writeFile('game_json.txt', JSON.stringify(mainData, null, 4), (err) => {
        if (err) throw err;
        console.log('File created/updated successfully.');
      });
}

testMod();