function remove_mustages(){
    // Removes existing mustaches if exists.
    var childIMGs = document.getElementById('resultDiv').getElementsByTagName('img');

    for( i=0; i< childIMGs.length; i++ )
    {
        var childIMG = childIMGs[i];
        if (childIMG.id != 'resultImage'){
            childIMG.remove()
        }
    }
};

function transformSnor(singleSnorBox, specificSnorData) {
    /* The snorboxen are determined for every face, each snor is allowed to go outside of the snorbox
    by a set amount left-rigth, top, and bottom. */

    let correctedSnorBox = Object.assign({}, singleSnorBox);
    correctedSnorBox['x'] = Math.round(singleSnorBox['x'] + singleSnorBox['width'] * ((1-specificSnorData['width_cor_factor'])/2))
    correctedSnorBox['width'] = Math.round(singleSnorBox['width'] * specificSnorData['width_cor_factor'])
    correctedSnorBox['y'] = Math.round(singleSnorBox['y'] + singleSnorBox['height'] * specificSnorData['height_cor_factor_up'])
    correctedSnorBox['height'] = Math.round(singleSnorBox['height'] * (1-specificSnorData['height_cor_factor_down']))

    return correctedSnorBox
};

function drawSnor(correctedSnorBox, snorSrc) {
    /* This function removes already existing snorren and replaces with new ones. */
    remove_mustages()

    var snor = document.createElement("IMG");
    snor.src = snorSrc
    snor.style.position = "absolute"
    snor.style.left=`${correctedSnorBox['x']}px`
    snor.style.top=`${correctedSnorBox['y']}px`
    snor.style.width=`${correctedSnorBox['width']}px`  
    snor.style.height=`${correctedSnorBox['height']}px`
    document.getElementById('resultDiv').appendChild(snor);
}
