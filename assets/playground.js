window.myNamespace = Object.assign({}, window.myNamespace, {
    tabulator: {
        cellLog: function (e, cell, table) {
            console.log("Cell got")
            console.log(e)
            console.log(cell)
        },
        // freeze a row with a double click
        rowDblClick : function(e, row, table) {

		    if(row.isFrozen()){
                row.unfreeze();
		    } else {
                row.freeze();
            }
        }
    }
});