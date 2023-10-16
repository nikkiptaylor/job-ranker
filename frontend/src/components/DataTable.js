import * as React from "react";
// import { DataGrid } from "@mui/x-data-grid";
import { AgGridReact } from "ag-grid-react"; // the AG Grid React Component

import "ag-grid-community/styles/ag-grid.css"; // Core grid CSS, always needed
import "ag-grid-community/styles/ag-theme-alpine.css"; // Optional theme CSS

const getColumns = (data) => {
  const columns = [];
  for (let key in data) {
    columns.push({ field: key, resizable: true, sortable: true, filter: true });
  }
  console.log(`Columns: ${columns}`);
  return columns;
};

export default function DataTable({ data }) {
  if (data) {
    const columns = getColumns(data[0]);
    // console.log(data);

    return (
      <div className="ag-theme-alpine" style={{ height: 500, width: 800 }}>
        <AgGridReact columnDefs={columns} rowData={data}></AgGridReact>
      </div>
    );
  } else {
    return null;
  }
}

// TODO convert to typescript
