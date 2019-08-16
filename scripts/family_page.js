$(document).ready(()=> {
    const family_id = $('#family_id').data('familyid')
    //const ratings = $('#ratings').data('ratings') 
    $.ajax({
        type: 'POST',
        url: '/get_data',
        data: `family_id=${family_id}`,
        success: ratings => {
            ratings = JSON.parse(ratings)
            let overall = 0
            ratings.forEach((el, index) => {
                let rating = 5
                if(el.times_rated > 0){
                    rating = Math.round(el.total_rating / el.times_rated)
                }
                
                overall += rating

                for(let y=6; y <= rating + 5; y++){
                    $(`#row_${index + 1}_star_${y}`).attr('src', '/images/star2.png')
                }
            })
            $('#family_rating').html(Math.round(100 * (overall / 5)) / 100)
        }
    })
    setInterval(() => {
        $.ajax({
            type: 'POST',
            url: '/get_data',
            data: `family_id=${family_id}`,
            success: ratings => {
                ratings = JSON.parse(ratings)
                let overall = 0
                for(let y=1; y <= 5; y++){
                    for(let x=6; x<= 10; x++){
                        $(`#row_${y}_star_${x}`).attr('src', '/images/star.png')
                    }
                }
                ratings.forEach((el, index) => {
                    let rating = 5
                    if(el.times_rated > 0){
                        rating = Math.round(el.total_rating / el.times_rated)
                    }
                    overall += rating
                    for(let y=6; y <= rating + 5; y++){
                        $(`#row_${index + 1}_star_${y}`).attr('src', '/images/star2.png')
                    }
                })
                $('#family_rating').html(Math.round(100 * (overall / 5)) / 100)
            }
        })
    },60 * 1000)

    const user_ratings = $('#user_ratings').data('userratings')
    user_ratings.forEach((el, index) => {
        if(el > 0){
            for(let y=1; y <= el; y++){
                $(`#row_${index + 1}_star_${y}`).attr('src', '/images/star2.png')
            }
        }
    })

    for(let i = 1;i <= 5;i++){
        let clicked = false
        let current_clicked = user_ratings[i-1]
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
                $.ajax({
                    type: "POST",
                    url: "/update",
                    data: `family_id=${family_id}&row=${i}&star=${x}`
                })
                console.log(`#row_${i}_star_${x}`)
            })
        }
    }
    $('#comments_submit').on('click', () => {
        let input = $('#comments_input').val()
        if(input){
            $('#comments_container').prepend(`
                <div class="comment">
                    ${input}
                </div>
            `)
            $.ajax({
                type: 'POST',
                url: '/comment',
                data: `family_id=${family_id}&content=${input}`
            })
        }
    })
})