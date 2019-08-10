$(document).ready(() => {
    const families = $('#families').data('families')
    $('#search').on('input', el => {
        $("#search_container").empty();
        let search = el.target.value.toLowerCase()
        if(search){
            let added = 0
            let results = families.map((family, index) => {
                let shortened_name = family.name.substring(0, search.length).toLowerCase()
                if(shortened_name == search) {
                    let new_div = `
                        <div id='result_${index}' class="search_result">
                            <div class='text'>${family.name}</div>
                            <div class='text'>${family.id}</div>
                            <form id='result_${index}_form' method='post' action='/'>
                                <input type='hidden' name='id' value='${family.id}'>
                            </form>
                        </div>
                    `
                    $('#search_container').append(new_div)
                    $(`#result_${index}`).on('click', () => {
                        $(`#result_${index}_form`).submit()
                    })
                    added++
                    return family
                }
            })
            if (added < 1){
                let new_div = `
                    <div class="search_result">
                        <div id='text'> No Result Found </div>
                    </div>
                `
                $('#search_container').append(new_div)
            }
        }
    })
})



