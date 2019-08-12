$(document).ready(() => {
    const families = $('#families').data('families')
    const states = $('#states').data('states')

    const states_keys = Object.keys(states)
    states_keys.forEach(el => {
      let new_option = `
        <option value='${el}'>
          ${el}
        </option>
      `
      $('#states_selection').append(new_option)
    })

    //$('#states_selection').append('')
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
                            <div class='text family_name'>${family.name}</div>
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
                    <div class="search_result no_result">
                        <div class='text no_result_text'> No Results Found </div>
                    </div>
                `
                $('#search_container').append(new_div)
            }
        }
    })
})
