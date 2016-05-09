function query_sights() {
    var area = $('#select_prov').find('option:selected').val();
    var month = $('#select_month').find('option:selected').val();
    var time = $('#time').find('option:selected').val();
    var _xsrf = $("input[name='_xsrf']").val();
    $.ajax({
        url: '/sights',
        type: 'POST',
        dataType: 'json',
        data: {
            'area': area,
            'month': month,
            'time': time,
            '_xsrf': _xsrf,
        },
        success: function(sights) {
            weight_list = sights['weight'];
            color_list = sights['color'];
            WordCloud(document.getElementById('my_canvas'),
                    {list: weight_list,
                        gridSize: 5,
                        weightFactor:2,
                        fontFamily: 'Average, Times, serif',
                        color: function(word){
                            colorStr = color_list[word];
                            rColor = parseInt(colorStr.substr(0,2), 16);
                            gColor = parseInt(colorStr.substr(2,2), 16);
                            bColor = parseInt(colorStr.substr(4,2), 16);
                            return "RGB("+[rColor, gColor, bColor].join(",") + ")";
                        },
                        rotateRatio: 0,
                    }
            );
        }
    });
}
