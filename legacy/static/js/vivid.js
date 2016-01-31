
var continueBtn = document.getElementById("continue");
var replayBtn = document.getElementById("replay");
var speechBox = document.getElementById("speech");
var valueH4 = document.getElementById("value");
var helperH4 = document.getElementById("helper");
var echoP = document.getElementById("echo");


//hide some infos
valueH4.style.display = "none";
replayBtn.style.display = "none";


var times = output.length;
var current = 0;
var displayStack = [];



function onKeyDown(event) {
    switch(event.keyCode) {
        case 39: nextStep();break;
        //case 37: previousStep();break;
    }
}

//register controller
document.addEventListener('keydown', onKeyDown, false);

//bind functions
continueBtn.onclick = nextStep;
replayBtn.onclick = replay;


function nextStep(event) {

    // check the two elements on the top of stack                                     
    if (displayStack.length >=2 && displayStack[displayStack.length-1][1] == displayStack[displayStack.length-2][1] && displayStack[displayStack.length-1][0] == displayStack[displayStack.length-2][0]) {

        displayStack.pop();
        var children = document.getElementById("speech").childNodes;
        speechBox.removeChild(children[children.length-1]);

        displayStack.pop();
        speechBox.removeChild(children[children.length-1]);
    }

    //over! display infos and enable replay btn
    if (current >= times) {
        valueH4.style.display = "block";
        continueBtn.style.display = "none";
        replayBtn.style.display = "block";
        
        echo(" ");
        return;
    }

    if (current == 0) {
        continueBtn.value = "next";
        helperH4.style.display = "none";
    }

    if (current>1 && output[current][0] < output[current-1][0]) {
        removeNode(output[current-1][0]);
    }


    
    //ask or answers
    if (output[current][3] == 0 || output[current][3] == 1) {    
        var newItem = document.createElement("div");
        newItem.innerHTML = output[current][2];
        if (output[current][3] == 0) { newItem.className = "talk ask"; }
        else { newItem.className = "talk answer" }

        //decorate
        switch(output[current][1]) { 
        case "func": newItem.className += " func";break;
        case "test":
        case "or":
        case "or1":
        case "or2":
        case "if":
        case "cond": newItem.className += " cond";break;
        case "begin":
        case "lambda":
        case "define":
        default: newItem.className += " ordinary";
        }
       
        //display some infomations
        switch(output[current][1]) { 
        case "or": echo("or asks 2 questions, one at a time. If the first one is true it stops and answers true. Otherwise it asks the second question and answers with whatever the second question answers.");break;
        case "cond": echo("cond asks a few questions, as long as the answer to one question is true, it stop asking more questions and return the value of evaluating the consequent expression of that question.");break;
        case "and": echo("and asks 2 questions, one at a time. If the first one is false it stops and answers false. Otherwise it askes the second question and answers with whatever the second question answers.");break;
        case "begin": echo("begin evaluates expressions in left-to-right order, and return the value of the last one.");break;
        case "func": echo("function call");break;
        default: echo(" ");
        }


        newItem.style.marginLeft = output[current][0]*15 + "px"
        speechBox.appendChild(newItem);
        displayStack.push(output[current]);
    } 
    current += 1;
    window.scroll(0,document.body.scrollHeight);

}


function previousStep(event) {
                                         
}


function replay(event) {
    current = 0;
    displayStack = [];
    valueH4.style.display = 'none';
    continueBtn.style.display = 'block';
    continueBtn.value = 'Start';
    replayBtn.style.display = 'none';
    helperH4.style.display = 'block';
    
}

function removeNode(depth) {
    for (var i=0; i<displayStack.length-1; i++) {
        // keep removing top elements
        if (displayStack[displayStack.length-1][0] == depth) {

            displayStack.pop();
            var children = document.getElementById("speech").childNodes;
            speechBox.removeChild(children[children.length-1]);
        } else {
            break;
        }
    }
}

function echo(str) {
    echoP.innerText = str;
                                           
}

