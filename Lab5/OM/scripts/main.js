function GetJobNumber() {
    let job_number = Number($('#job_number_input').val());

    if (isNaN(job_number) || job_number <= 0) {
        job_number = 3;
    }

    return job_number;
}

function GetWeights() {
    let weights = new Array();

    for (let i = 0; i < GetJobNumber(); i++) {
        let w = Number($('#weight_' + i + '').val());
        weights.push(w);
    }
    
    return weights;
}

function GetDurations() {
    let durations = new Array();

    for (let i = 0; i < GetJobNumber(); i++) {
        let d = Number($('#duration_' + i + '').val());
        durations.push(d);
    }
    
    return durations;
}

function GetMatrix() {
    let matrix = new Array();
    let n = GetJobNumber();

    for (let i = 0; i < GetJobNumber(); i++) {
        for (let j = 0; j < GetJobNumber(); j++) {
            let d = Number($('#' + i + '_' + j).hasClass("activated"));
            matrix.push(d);
        }
    }
    
    return matrix;
}

function ReloadMatrix() {
    let job_number = GetJobNumber();
    let matrix_field = $('div[id="field"]');

    matrix_field.empty();

    matrix_field.append( '<div class="row" id="0"></div>' );
    {
        let row_i = $('.row[id=0]');

        row_i.append( '<div class="ceil centered"><span> </span></div>' );

        for (let j = 0; j < job_number; j++) {
            row_i.append( '<div class="ceil matrix_ceil_header centered"><span>G' + j + '</span></div>' );
        }

        row_i.append( '<div class="ceil matrix_ceil_header centered"><span>W</span></div>' );
        row_i.append( '<div class="ceil matrix_ceil_header centered"><span>Duration</span></div>' );
    }
    
    for (let i = 1; i <= job_number; i++) {
        matrix_field.append( '<div class="row" id="' + i + '"></div>' );
        let row_i = $('.row[id=' + i + ']');

        row_i.append( '<div class="ceil centered"><span>J' + (i - 1) + ': </span></div>' );

        for (let j = 0; j < job_number; j++) {
            row_i.append( '<div class="ceil matrix_ceil"><button class="bt_ceil" id="' + (i - 1) + '_' + j + '"></div>' );
        }

        row_i.append( '<div class="ceil matrix_ceil"><input value="1" class="inp_ceil weight" id="weight_' + (i - 1) + '"></div>' );
        row_i.append( '<div class="ceil matrix_ceil"><input value="1" class="inp_ceil duration" id="duration_' + (i - 1) + '"></div>' );

        $('#' + (i-1) + '_0').addClass("activated");
    }
}

function DrawShedule() {

    let weights = GetWeights();
    let durations = GetDurations();
    let matrix = GetMatrix();
    let n = GetJobNumber();
    
    let canvas = document.getElementById("canvas");
    let ctx = canvas.getContext("2d");

    canvas.width = 4 * canvas.getBoundingClientRect().width;
    canvas.height = 4 * canvas.getBoundingClientRect().height;

    // Background
    ctx.fillStyle = "#f0ffff";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.lineWidth = 5;
    ctx.fillStyle = "#ffffff";

    let group_duration = Array(n).fill(0);
    let sum_durations = 0;

    for (let j = 0; j < n; j++) {
        for (let i = 0; i < n; i++) {
            if (matrix[i * n + j] == 1) {
                group_duration[j] += durations[i];
                sum_durations += durations[i];
            }
        }
    }

    
    let tau = 1;
    let start = 0;
    let draw_start = 5;
    let BlockHeight = 300;
    let BlockWidth = canvas.width / (sum_durations + n);
    let draw_tau = BlockWidth / 10;

    let score = 0;

    let had_be_drawn = 0;

    for (let j = 0; j < n; j++) {
        if (had_be_drawn < n) {
            ctx.fillStyle = "#aaaaff";
            ctx.strokeStyle = "#aaaaff";
            console.log("Draw:", draw_start, draw_start + draw_tau);
            ctx.fillRect(draw_start, 245, draw_tau+5, BlockHeight + 8);

            ctx.strokeStyle = "#000000";
        }
        
        draw_start += draw_tau;
        start += tau;

        let group_weight = 0;

        for (let i = 0; i < n; i++) {
            if (matrix[i * n + j] == 1) {
                had_be_drawn++;
                ctx.fillStyle = "#ff7070";
                ctx.fillRect(draw_start, 250, durations[i] * BlockWidth, BlockHeight);
                ctx.strokeRect(draw_start, 250, durations[i] * BlockWidth, BlockHeight);
                
                ctx.textAlign="center";
                ctx.textBaseline = "middle";
                ctx.font = "80px sans-serif"; 
                ctx.fillStyle = "black"; 
                ctx.fillText("J" + i, draw_start + durations[i] * BlockWidth / 2, 250 + BlockHeight / 2);
                draw_start += durations[i] * BlockWidth;
                start += durations[i];
                group_weight += weights[i];
            }
        }

        score += start * group_weight;
    }

    ctx.fillText("Score: "+score, 240, 80);

    // Axes X
    ctx.lineWidth = 15;
    ctx.beginPath();
    ctx.moveTo(0, canvas.height);
    ctx.lineTo(canvas.width, canvas.height);
    ctx.stroke();

    // Axes Y 
    ctx.beginPath();
    ctx.moveTo(0, canvas.height);
    ctx.lineTo(0, 0);
    ctx.stroke();
}

$("body", document).ready(function() {

    $('#btn_reload').click(function(){
        ReloadMatrix();

        $('button.bt_ceil').click(function() {
            let i_j = this.id.split('_');
            let i = i_j[0];
            let j = i_j[1];
            
            for (let k = 0; k < GetJobNumber(); k++) {
                $('#' + i + '_' + k).removeClass("activated");
            }
    
            $('#' + i + '_' + j).toggleClass("activated");
    
            DrawShedule();
        });

        DrawShedule();

        $('input[id!=job_number_input]').on('input', function() {
            DrawShedule();
        });
    });

    $('input[id!=job_number_input]').on('input', function() {
        DrawShedule();
    });


    $('#btn_reload').click();
});


