
function setCoolTool() {
    var cooltool = $('.cooltool');

    cooltool.each(function() {
        var el = $(this);
        if(!el.find('.tooltip').length > 0) {
            el.append('<span class="tooltip" data-tooltip="'+el.attr('data-tooltip-dir')+'"><span class="before-content">'+el.attr('data-content-before').replace(/\/n/g, "<br>")+'</span><span class="after-content">'+el.attr('data-content-after')+'</span></span>');
        }
    });

    $(document).on('click', '.cooltool', function() {
        var el = $(this);
        var tool = $(this).find('.tooltip');
        var b = el.find('.before-content');
        var a = el.find('.after-content');
        if (el.attr('data-content-after') != undefined) {
            if (el.attr('data-keep-after') == 'true' || el.attr('data-keep-after') == '') {
                a.addClass('showTip');
                b.addClass('hideTip');
            } else {
                function changeContent() {
                    b.addClass('hideTip').delay(1200).queue(function(next){
                        b.removeClass('hideTip');
                        next();
                    });
                    a.addClass('showTip').delay(1200).queue(function(next){
                        a.removeClass('showTip');
                        next();
                    });
                } changeContent();
            }
        }
    });

    $(document).on('mouseleave', '.cooltool', function() {
        console.log('touchend');
        var el = $(this);
        var b = el.find('.before-content');
        var a = el.find('.after-content');
        function revertChange() {
            a.delay(300).queue(function(next){
                a.addClass('hideTip').removeClass('showTip');
                a.removeClass('hideTip');
                next();
            });
            b.delay(300).queue(function(next){
                b.addClass('showTip').removeClass('hideTip');
                b.removeClass('showTip');
                next();
            });
        } revertChange();
    });
    
} setCoolTool();
    