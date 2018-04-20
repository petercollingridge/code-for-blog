// Matrix variables consist of a coefficient and a name, e.g. 3a
// If the name is undefined, then we have a simple number.
// If the coefficient is undefined, then assume it is 1.
function MatrixVariable(coefficient, name) {
    this.coefficient = coefficient;
    
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
        this.neg_display = "-" + this.name;
    } else if (this.coefficient === -1) {
        this.display = "-" + this.name;
        this.neg_display = this.name;
    } else {
        this.display = this.coefficient + this.name;
        this.neg_display = -this.coefficient + this.name;
    }
};

MatrixVariable.parseVariable = function(input_string) {
    var re_variable = /([-+])?(\d*\.?\/?\d+)?\s*([a-zA-Z\(\)]*)?/g;
    var variable_terms = re_variable.exec(input_string);
    var sign = variable_terms[1] === '-' ? -1 : 1;
    var coefficient = typeof variable_terms[2] !== 'undefined' ? parseFloat(variable_terms[2]) : 1;
    return new MatrixVariable(sign * coefficient, variable_terms[3]);
}

MatrixVariable.prototype.add = function(that) {
    var name, coefficient;

    if (this.name === that.name) {
        name = this.name;
        coefficient = this.coefficient + that.coefficient;
    } else if (this.coefficient === 0) {
        name = that.name;
        coefficient = that.coefficient;
    } else if (that.coefficient === 0) {
        name = this.name;
        coefficient = this.coefficient;
    } else {
        coefficient = 1;
        if (that.coefficient > 0) {
            name = this.display + " + " + that.display;
        } else {
            name = this.display + " - " + that.neg_display;
        }
    }
    return new MatrixVariable(coefficient, name);
};

MatrixVariable.prototype.multiply = function(that) {
    var name;
    var coefficient = this.coefficient * that.coefficient;
    
    if (this.name === "") {
        name = that.name;
    } else if (that.name === "") {
        name = this.name;
    } else {
        name = this.name + " * " + that.name;   
    }
    return new MatrixVariable(coefficient, name);
}

function Matrix(position, matrixType, values) {
    this.position = position;
    this.type = matrixType;
    this.values = [];
    this.setValues(values);
};

Matrix.prototype.display = function() {
    // Write dimensions
    if (this.position != 2) {
        $('#matrix-' + this.position + '-dim-0').val(this.values.length);
        $('#matrix-' + this.position + '-dim-1').val(this.values[0].length);
    } else {
        $('#matrix-' + this.position + '-dim-0').html(this.values.length);
        $('#matrix-' + this.position + '-dim-1').html(this.values[0].length);
    }
    
    var element = $('#matrix-' + this.position);
    var matrix = element.find('.matrix-columns');
    var name = 'matrix-value-' + this.position + '-';
    
    // Clear current values
    matrix.empty();

    for (var i = 0; i < this.values[0].length; i++) {
        // Create columns
        var column = $('<span class="matrix-column"></span>');
        matrix.append(column);
        
        // Create items
        for (var j = 0; j < this.values.length; j++) {
            var item = this.createMatrixItem(this.values[j][i].display);
            item.attr('id', name + j + '-' + i).appendTo(column);
        }
    }
};

Matrix.prototype.setValues = function(values) {
    this.values = [];
    
    for (var i = 0; i < values.length; i++) {
        var row = [];
        for (var j = 0; j < values[0].length; j++) {
            row.push(MatrixVariable.parseVariable(values[i][j]));
        }
        this.values.push(row);
    }
};

Matrix.prototype.createMatrixItem = function(value) {
    var item = $('<span class="matrix-item">' + value + '</span>');
    if (this.type === 'input') {
        item.attr('contenteditable', true);
    }

    return item
};

Matrix.prototype.resize = function(dimension, size) {        
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
            for (var j = 0; j < size - n; j++) {
                var newRow = [];
                for (var i = 0; i < m; i++) {
                    newRow.push(new MatrixVariable(0))
                };
                this.values.push(newRow);
            }
        }
    } else {
        // Change number of columns
        if (size < m) {
            // Remove columns
            for (var i = 0; i < n; i++) {
                this.values[i] = this.values[i].slice(0, size);
            }
        } else {
            // Add columns
            for (var i = 0; i < n; i++) {
                for (var j = 0; j < size - m; j++) {
                    this.values[i].push(new MatrixVariable(0));
                }
            }
        }
    }
    this.display();
}

var multiplyMatrices = function() {
    var values1 = matrices[0].values;
    var values2 = matrices[1].values;
    var result = []

    for (var i = 0; i < values1.length; i++) {
        row = [];
        for (var j = 0; j < values2[0].length; j++) {
            var value = new MatrixVariable(0);
            for (var k = 0; k < values1[0].length; k++){
                value = value.add(values1[i][k].multiply(values2[k][j]));
            }
            row.push(value);
        }
        result.push(row);
    }

    resultMatrix.values = result;
    resultMatrix.display(); 
};

var initialiseMatrices = function (m1, m2) {
    matrices[0].setValues(m1);
    matrices[1].setValues(m2);
    
    matrices[0].display();
    matrices[1].display();
    multiplyMatrices();
    createInputHandlers($('.matrix-item'), handleMatrixInput);
    createInputHandlers($('.dimension'), handleDimensionInput);
};

// When a value is entered into a matrix update the matrix and multiply
var handleMatrixInput = function(evt) {
    var value = MatrixVariable.parseVariable($(this).text());
    
    // Set text to parsed value in case they are different
    $(this).text(value.display);

    // Update the relevant value of the matrix object
    var pos = $(this).attr('id').split('-');

    matrices[pos[2]].values[pos[3]][pos[4]] = value;
    multiplyMatrices();
};

var handleDimensionInput = function(evt) {
    var value = parseFloat($(this).val());

    if (isNaN(value)) { value = 0; }
    else if (value < 1) { value = 1; }
    else if (value > 6) { value = 6; }

    $(this).val(value)

    // update the relevant value of the matrix object
    var pos = $(this).attr('id').split('-');
    matrices[pos[1]].resize(pos[3], value);

    // Resize other matrix so multiplication still works
    if (pos[1] !== pos[3]) {
        matrices[pos[3]].resize(pos[1], value);
    }

    createInputHandlers($('.matrix-item'), handleMatrixInput);
    multiplyMatrices();
};

var createInputHandlers = function(inputBox, parseResult) {    
    // Select text when input focussed
    inputBox.click(function(evt) { $(this).select(); });
    
    // What to do when result is entered
    inputBox.on('parseResult', parseResult);
    
    // Calculate new matrix when input complete
    inputBox.blur(function(evt) { $(this).trigger('parseResult'); });
    
    // Pressing enter removes focus from box
    inputBox.keypress(function(evt) {
        if (evt.which === 13) {
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
        initialiseMatrices([['-a', 'b'], [3, 'c']],
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