function transformSnor(snorBox, snorName) {
    /* The snorboxen are determined for every face, each snor is allowed to go outside of the snorbox
    by a set amount left-rigth, top, and bottom. */
    var snorData = snorTypes[snorName]

    let correctedSnorBox = Object.assign({}, snorBox);
    correctedSnorBox['x'] = snorBox['x'] + snorBox['width'] * ((1-snorData['width_cor_factor'])/2)
    correctedSnorBox['width'] = snorBox['width'] * snorData['width_cor_factor']
    correctedSnorBox['y'] = snorBox['y'] + snorBox['height'] * (1 - snorData['height_cor_factor_up'])
    correctedSnorBox['height'] = snorBox['height'] * (1-snorData['height_cor_factor_down'])

    return correctedSnorBox
};

function drawSnorren(correctedSnorBox, snorSrc) {
    /* This function removes already existing snorren and replaces with new ones. */
    var snor = document.createElement("IMG");
    snor.src = snorSrc
    snor.style.position = "absolute"
    snor.style.left=`${correctedSnorBox['x']}px`
    snor.style.top=`${correctedSnorBox['y']}px`
    snor.style.width=`${correctedSnorBox['width']}px`  
    snor.style.height=`${correctedSnorBox['height']}px`
    document.getElementById('resultDiv').appendChild(snor);
}