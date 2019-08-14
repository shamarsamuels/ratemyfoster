$(document).ready(()=> {
    for(let i = 1;i <= 5;i++){
        let clicked = false
        let current_clicked = 0
        for(let x = 1;x <= 5;x++){
            let star = $(`#row_${i}_star_${x}`)
            star.hover(() => {
                for(let y=1; y <= x; y++){
                    $(`#row_${i}_star_${y}`).attr('src', '/images/star2.png')
                }
            }, () => {
                if(!clicked || x > current_clicked){
                    for(let y=current_clicked + 1; y <= x; y++){
                        $(`#row_${i}_star_${y}`).attr('src', '/images/star.png')
                    }
                }
            })
            star.click(() => {
                clicked = true
                current_clicked = x
                for(let y=1; y <= 5; y++){
                    $(`#row_${i}_star_${y}`).attr('src', '/images/star.png')
                }
                for(let y=1; y <= x; y++){
                    $(`#row_${i}_star_${y}`).attr('src', '/images/star2.png')
                }
                console.log(`#row_${i}_star_${x}`)
            })
        }
    }
})