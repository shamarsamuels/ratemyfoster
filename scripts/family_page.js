$(document).ready(()=> {
    for(let i = 1;i <= 5;i++){
        for(let x = 1;x <= 5;x++){
            let star = $(`#row_${i}_star_${x}`)
            star.hover(() => {
                for(let y=1; y <= x; y++){
                    $(`#row_${i}_star_${y}`).attr('src', '/images/star2.png')
                }
            }, () => {
                for(let y=1; y <= x; y++){
                    $(`#row_${i}_star_${y}`).attr('src', '/images/star.png')
                }
            })
            star.click(() => {
                console.log('Clicked')
            })
        }
    }
})