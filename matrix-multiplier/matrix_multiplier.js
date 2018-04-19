function MatrixVariable(coefficient, name) {
    this.coefficient = typeof coefficient !== 'undefined' ? parseFloat(coefficient) : 1;
    
    if (this.coefficient === 0 || typeof name === 'undefined') {
        this.name = "";
    } else {
        this.name = name;
    }
    
    if (this.name === ""){
        this.display = this.coefficient;
        this.neg_display = -this.coefficient;
    } else if (this.coefficient === 1) {
        this.display = this.name;
    } else if (this.coefficient === -1) {
        this.display = "-" + this.name;
        this.neg_display = this.name;
    } else {
        this.display = this.coefficient + this.name;
        this.neg_display = -this.coefficient + this.name;
    }
};

var parseVariable = function(input_string) {
    var re_variable = /([-+]?\d*\.?\/?\d+)?([a-zA-Z\(\)]*)?/g;
    var variable_terms = re_variable.exec(input_string);
    return new MatrixVariable(variable_terms[1], variable_terms[2]);
}

var fixWidth = function(element) {
        var text_value = element.val();
        if (text_value == '') text_value = 0;

        var html_text = $('<span id="find-width" class="matrix-item">' + text_value + '</span>');
        $(document.body).append(html_text);
        var width = $('#find-width').width() + 2;

        element.css({width: width});
        html_text.remove();
}

function Matrix(position, matrixType, values) {
    this.position = position;
    var createInputElement;
    this.values = [];
    
    this.addValues = function(values) {
        this.values = [];
        
        for (var i=0; i < values.length; i++) {
            var row = [];
            for (var j=0; j < values[0].length; j++) {
                row.push(parseVariable(values[i][j]));
            }
            this.values.push(row);
        }
    };
    
    this.addValues(values);
    
    if (matrixType === 'input' ) {
        createInputElement = function(value) {
            return '<input class="matrix-item" value="' + value + '"/>';
        };
    } else {
        createInputElement = function(value) {
            return '<div class="matrix-item">' + value + '</div>';
        };
    }
    
    this.display = function() {
        // Write dimensions
        if (this.position != 2) {
            $('#matrix-' + this.position + '-dim-0').val(this.values.length);
            $('#matrix-' + this.position + '-dim-1').val(this.values[0].length);
        } else {
            $('#matrix-' + this.position + '-dim-0').html(this.values.length);
            $('#matrix-' + this.position + '-dim-1').html(this.values[0].length);
        }
        
        var element = $('#matrix-' + this.position);
        var values = $('#matrix-' + this.position + '>.matrix-columns')
        var name = 'matrix-value-' + this.position + '-';
        
        values.empty();
        for (var i=0; i < this.values[0].length; i++) {
            var column = $('<div class="matrix-column"></div>');
            values.append(column);
            
            for (var j=0; j < this.values.length; j++) {
                var item = $(createInputElement(this.values[j][i].display));
                item.attr('id', name + j + '-' + i);
                column.append(item);

                // Fix the width when first setting up input matrices
                if (position < 2) { fixWidth(item); }
            }
        }
        
        var column_height = column.height();
        element.css({height: column_height + 3});
    };

    this.resizeMatrix = function(dimension, size){        
        // Change dimension to new size
        
        var n = this.values.length;
        var m = this.values[0].length;
        
        if (dimension === '0' ) {
            // Change number of rows
            if (size < n) {
                // Remove rows
                this.values = this.values.slice(0, size);
            } else {
                // Add rows of zeros
                for (var j=0; j < size - n; j++) {
                    var new_row = [];
                    for (var i=0; i < m; i++) { new_row.push(new MatrixVariable(0)) };
                    this.values.push(new_row);
                }
            }
        } else {
            // Change number of columns
            if (size < m) {
                // Remove columns
                for (var i=0; i < n; i++) {
                    this.values[i] = this.values[i].slice(0, size);
                }
            } else {
                // Add columns
                for (var i=0; i < n; i++) {
                    for (var j=0; j < size - m; j++) {
                        this.values[i].push(new MatrixVariable(0));
                    }
                }
            }
        }
        this.display();
    }
};

var multiplyVariables = function(v1, v2) {
    var coefficient = v1.coefficient * v2.coefficient;
    
    if (v1.name === "") {
        var name = v2.name;
    } else if (v2.name === "") {
        var name = v1.name;
    } else {
        var name = v1.name + "." + v2.name;   
    }
    return new MatrixVariable(coefficient, name);
}

var addVariables = function(v1, v2) {
    if (v1.name === v2.name) {
        var name = v1.name;
        var coefficient = v1.coefficient + v2.coefficient;
    } else if (v1.coefficient === 0) {
        var name = v2.name;
        var coefficient = v2.coefficient;
    } else if (v2.coefficient === 0) {
        var name = v1.name;
        var coefficient = v1.coefficient;
    } else {
        if (v2.coefficient > 0) { var name = v1.display + " + " + v2.display; }
        else { var name = v1.display + " - " + v2.neg_display; }
        
        var coefficient = 1;
    }
    return new MatrixVariable(coefficient, name);
}

var multiplyMatrices = function() {   
    var values1 = matrices[0].values;
    var values2 = matrices[1].values;
    var result = []

    for (var i=0; i < values1.length; i++) {
        row = [];
        for (var j=0; j < values2[0].length; j++) {
            var value = new MatrixVariable(0);
            for (var k=0; k < values1[0].length; k++){
                value = addVariables(value, multiplyVariables(values1[i][k], values2[k][j]));
            }
            row.push(value);
        }
        result.push(row);
    }
    resultMatrix.values = result;
    resultMatrix.display(); 
};

var initialiseMatrices = function (m1, m2) {
    matrices[0].addValues(m1);
    matrices[1].addValues(m2);
    
    matrices[0].display();
    matrices[1].display();
    multiplyMatrices();
    createInputHandlers($('input.matrix-item'), handleMatrixInput);
    createInputHandlers($('input.dimension'), handleDimensionInput);
};

// When a value is entered into a matrix undate the matrix and multiply
var handleMatrixInput = function(evt) {
    var value = parseVariable($(this).val());
    $(this).val(value.display);

    // update the relevant value of the matrix object
    var pos = $(this).attr('id').split('-');
    matrices[pos[2]].values[pos[3]][pos[4]] = value;

    $(this).trigger('keyup');   // Fix width
    multiplyMatrices();
};

var handleDimensionInput = function(evt) {
    var value = parseFloat($(this).val());
    if (isNaN(value)) value = 0;
    $(this).val(value)
    if (value < 1) value = 1;
    if (value > 6) value = 6;

    // update the relevant value of the matrix object
    var pos = $(this).attr('id').split('-');
    matrices[pos[1]].resizeMatrix(pos[3], value);

    // Resize other matrix so multiplication still works
    if (pos[1] != pos[3]) {
        matrices[pos[3]].resizeMatrix(pos[1], value);
    }
    createInputHandlers($('input.matrix-item'), handleMatrixInput);
    multiplyMatrices();
};

var createInputHandlers = function(inputBox, parseResult) {    
    // Select text when input focussed
    inputBox.click(function(evt) { $(this).select(); });
    
    // What to do when result is entered
    inputBox.on('parseResult', parseResult );
    
    // Recalculate width when new value is entered - should recalculate matrix too
    inputBox.keyup(function(evt) { fixWidth($(this)) });
    
    // Calculate new matrix when input complete
    inputBox.blur(function(evt) { $(this).trigger('parseResult'); });
    
    // Pressing enter removes focus from box
    inputBox.keypress(function(evt) {
        if(evt.which == 13) {
            $(this).blur();
        }
    });
};

var createExampleButtons = function() {
    $('#example-matrix-1').click(function() {
        $('.example-matrix').removeClass("selected");
        $(this).addClass("selected");
        initialiseMatrices([[1,2], [3,4], [5,6]],
                            [[1,0], [0,1]]);
    });
    $('#example-matrix-2').click(function(){
        $('.example-matrix').removeClass("selected");
        $(this).addClass("selected");
        initialiseMatrices([[1, -2.01, 3.14], [0.499, -5, -0.6]],
                           [[2, 2.5], [-0.275, -3], [-3.25, 0.3]]);
    });
    $('#example-matrix-3').click(function(){
        $('.example-matrix').removeClass("selected");
        $(this).addClass("selected");
        initialiseMatrices([['a', 'b'], [3, 'c']],
                           [['a', 2], ['b', 'c']]);
    });
    $('#example-matrix-4').click(function(){
        $('.example-matrix').removeClass("selected");
        $(this).addClass("selected");
        initialiseMatrices([['sin(t)', 'a'], ['0.5a', -1], [1.5, '-4a']],
                           [['3a', 'a'], [2, 'cos(t)']]);
    });
};

var matrices = [new Matrix(0, 'input', [[1]]),
                new Matrix(1, 'input', [[1]])];
var resultMatrix = new Matrix(2, 'output', [[1]]);

$(document).ready(function() {
    createExampleButtons();
    $('#example-matrix-1').click();
});