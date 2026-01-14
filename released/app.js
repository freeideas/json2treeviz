// JSON Tree Visualizer Application

let cy = null; // Cytoscape instance
let collapsedNodes = new Set(); // Track collapsed nodes

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    const jsonInput = document.getElementById('json-input');
    const filePicker = document.getElementById('file-picker');
    const filePickerButton = document.getElementById('file-picker-button');
    const visualizeButton = document.getElementById('visualize-button');
    const toggleFormButton = document.getElementById('toggle-form');
    const inputForm = document.getElementById('input-form');

    // $REQ_JSON_INPUT_007: Example Data Pre-loaded on Page Load
    fetch('example-data.json')
        .then(response => response.json())
        .then(exampleData => {
            jsonInput.value = JSON.stringify(exampleData, null, 4);
        })
        .catch(error => {
            console.error('Failed to load example data:', error);
        });

    // $REQ_JSON_INPUT_002: Drag-and-Drop Zone
    // $REQ_JSON_INPUT_004: Drag-and-Drop Populates Textarea
    jsonInput.addEventListener('dragover', function(e) {
        e.preventDefault();
        e.stopPropagation();
    });

    jsonInput.addEventListener('drop', function(e) {
        e.preventDefault();
        e.stopPropagation();

        const files = e.dataTransfer.files;
        if (files.length > 0) {
            const file = files[0];
            if (file.name.endsWith('.json')) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    // $REQ_INPUT_FORM_002: No Immediate Action on Paste or Drop
                    jsonInput.value = e.target.result;
                };
                reader.readAsText(file);
            }
        }
    });

    // $REQ_JSON_INPUT_003: File Picker
    filePickerButton.addEventListener('click', function() {
        filePicker.click();
    });

    filePicker.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                // $REQ_INPUT_FORM_002: No Immediate Action on Paste or Drop
                jsonInput.value = e.target.result;
            };
            reader.readAsText(file);
        }
    });

    // $REQ_JSON_INPUT_006: Visualize Button
    // $REQ_INPUT_FORM_003: Visualize Button Collapses Form and Renders Tree
    visualizeButton.addEventListener('click', function() {
        const jsonText = jsonInput.value.trim();
        if (!jsonText) {
            alert('Please enter or load JSON data');
            return;
        }

        try {
            // $REQ_TRANSFORM_001: Parse JSON Text
            const jsonData = JSON.parse(jsonText);

            // Collapse the form
            inputForm.style.display = 'none';
            toggleFormButton.style.display = 'inline-block';
            document.getElementById('tree-container').style.display = 'block';

            // Render the tree
            renderTree(jsonData);
        } catch (error) {
            alert('Invalid JSON: ' + error.message);
        }
    });

    // $REQ_INPUT_FORM_004: Collapsed Form Can Be Expanded
    toggleFormButton.addEventListener('click', function() {
        if (inputForm.style.display === 'none') {
            inputForm.style.display = 'block';
            toggleFormButton.textContent = 'Hide Input';
        } else {
            inputForm.style.display = 'none';
            toggleFormButton.textContent = 'Edit Input';
        }
    });
});

// $REQ_TRANSFORM_008: Parent ID Field Pattern Matching
function findParentIdField(obj) {
    const pattern = /^parent[^a-zA-Z0-9]?id$/i;
    for (const key in obj) {
        if (pattern.test(key)) {
            return key;
        }
    }
    return null;
}

// $REQ_TRANSFORM_007: Hierarchy Override for Arrays of Objects with id/parent_id
function isHierarchyArray(arr) {
    if (!Array.isArray(arr) || arr.length === 0) {
        return false;
    }

    // Check if all elements are objects with id and parent id field
    for (const item of arr) {
        if (typeof item !== 'object' || item === null || Array.isArray(item)) {
            return false;
        }
        if (!('id' in item)) {
            return false;
        }
        if (!findParentIdField(item)) {
            return false;
        }
    }

    return true;
}

// Convert JSON to Cytoscape elements
function jsonToElements(data, parentId = null, key = 'root') {
    const elements = [];
    let nodeId = 'node_' + Math.random().toString(36).substr(2, 9);

    // $REQ_TRANSFORM_007: Hierarchy Override for Arrays of Objects with id/parent_id
    if (Array.isArray(data) && isHierarchyArray(data)) {
        // Handle hierarchy array specially
        const parentIdField = findParentIdField(data[0]);

        // Create nodes for all items
        const idToNodeId = {};
        data.forEach(item => {
            const itemNodeId = 'node_' + Math.random().toString(36).substr(2, 9);
            idToNodeId[item.id] = itemNodeId;

            // $REQ_TRANSFORM_003: Primitive Fields as Labels
            // $REQ_NODE_LABELS_001: Primitive Fields Displayed as Labels
            // $REQ_TRANSFORM_004: Null Fields Not Shown
            // $REQ_NODE_LABELS_002: Null Values Excluded from Labels
            const label = buildLabel(item);

            elements.push({
                data: {
                    id: itemNodeId,
                    label: label,
                    rawData: item
                }
            });
        });

        // Create edges based on parent relationships
        // $REQ_TRANSFORM_009: Parent/Child Relationship by ID Matching
        data.forEach(item => {
            const itemNodeId = idToNodeId[item.id];
            const parentIdValue = item[parentIdField];

            if (parentIdValue && idToNodeId[parentIdValue]) {
                elements.push({
                    data: {
                        source: idToNodeId[parentIdValue],
                        target: itemNodeId
                    }
                });
            } else if (parentId) {
                // If no parent in array, attach to parent node
                elements.push({
                    data: {
                        source: parentId,
                        target: itemNodeId
                    }
                });
            }
        });

        // Process nested objects and arrays in each item
        data.forEach(item => {
            const itemNodeId = idToNodeId[item.id];
            for (const itemKey in item) {
                const value = item[itemKey];
                // $REQ_TRANSFORM_005: Nested Objects and Arrays Become Children
                if (typeof value === 'object' && value !== null) {
                    const childElements = jsonToElements(value, itemNodeId, itemKey);
                    elements.push(...childElements);
                }
            }
        });

        return elements;
    }

    // $REQ_TRANSFORM_002: Objects Become Nodes
    if (typeof data === 'object' && data !== null && !Array.isArray(data)) {
        // $REQ_TRANSFORM_003: Primitive Fields as Labels
        // $REQ_NODE_LABELS_001: Primitive Fields Displayed as Labels
        const label = buildLabel(data);

        elements.push({
            data: {
                id: nodeId,
                label: label || key,
                rawData: data
            }
        });

        if (parentId) {
            elements.push({
                data: {
                    source: parentId,
                    target: nodeId
                }
            });
        }

        // Process nested objects and arrays
        for (const childKey in data) {
            const value = data[childKey];
            // $REQ_TRANSFORM_005: Nested Objects and Arrays Become Children
            if (typeof value === 'object' && value !== null) {
                const childElements = jsonToElements(value, nodeId, childKey);
                elements.push(...childElements);
            }
        }

        return elements;
    }

    // $REQ_TRANSFORM_006: Arrays Become Nodes with Element Children
    if (Array.isArray(data)) {
        elements.push({
            data: {
                id: nodeId,
                label: key + ' [' + data.length + ']',
                rawData: data
            }
        });

        if (parentId) {
            elements.push({
                data: {
                    source: parentId,
                    target: nodeId
                }
            });
        }

        data.forEach((item, index) => {
            if (typeof item === 'object' && item !== null) {
                const childElements = jsonToElements(item, nodeId, '[' + index + ']');
                elements.push(...childElements);
            } else {
                // Primitive array element
                const childNodeId = 'node_' + Math.random().toString(36).substr(2, 9);
                elements.push({
                    data: {
                        id: childNodeId,
                        label: '[' + index + ']: ' + String(item),
                        rawData: item
                    }
                });
                elements.push({
                    data: {
                        source: nodeId,
                        target: childNodeId
                    }
                });
            }
        });

        return elements;
    }

    // Primitive values
    elements.push({
        data: {
            id: nodeId,
            label: key + ': ' + String(data),
            rawData: data
        }
    });

    if (parentId) {
        elements.push({
            data: {
                source: parentId,
                target: nodeId
            }
        });
    }

    return elements;
}

// $REQ_TRANSFORM_003: Primitive Fields as Labels
// $REQ_TRANSFORM_004: Null Fields Not Shown
// $REQ_NODE_LABELS_001: Primitive Fields Displayed as Labels
// $REQ_NODE_LABELS_002: Null Values Excluded from Labels
function buildLabel(obj) {
    const labels = [];
    for (const key in obj) {
        const value = obj[key];
        // Only primitive fields, excluding null
        if (value !== null && (typeof value === 'string' || typeof value === 'number' || typeof value === 'boolean')) {
            labels.push(key + ': ' + String(value));
        }
    }
    return labels.join('\n') || '{}';
}

// $REQ_TREE_RENDERING_001: Render JSON as Tree
function renderTree(jsonData) {
    const container = document.getElementById('tree-container');

    // Convert JSON to Cytoscape elements
    const elements = jsonToElements(jsonData);

    // Initialize Cytoscape
    cy = cytoscape({
        container: container,
        elements: elements,
        style: [
            {
                selector: 'node',
                style: {
                    'label': 'data(label)',
                    'text-valign': 'center',
                    'text-halign': 'center',
                    'background-color': '#0074D9',
                    'color': '#fff',
                    'text-wrap': 'wrap',
                    'text-max-width': '200px',
                    'width': 'label',
                    'height': 'label',
                    'padding': '10px',
                    'shape': 'roundrectangle'
                }
            },
            {
                selector: 'edge',
                style: {
                    'width': 2,
                    'line-color': '#ccc',
                    'target-arrow-color': '#ccc',
                    'target-arrow-shape': 'triangle',
                    'curve-style': 'bezier'
                }
            },
            {
                selector: '.collapsed',
                style: {
                    'background-color': '#FF851B'
                }
            }
        ],
        layout: {
            name: 'breadthfirst',
            directed: true,
            padding: 10,
            spacingFactor: 1.5
        }
    });

    // $REQ_TREE_RENDERING_007: Nodes Are Collapsible
    cy.on('tap', 'node', function(evt) {
        const node = evt.target;
        const nodeId = node.id();

        if (collapsedNodes.has(nodeId)) {
            // Expand
            collapsedNodes.delete(nodeId);
            node.removeClass('collapsed');
            // Show descendants
            showDescendants(node);
        } else {
            // Collapse
            collapsedNodes.add(nodeId);
            node.addClass('collapsed');
            // Hide descendants
            hideDescendants(node);
        }

        // Re-layout
        cy.layout({
            name: 'breadthfirst',
            directed: true,
            padding: 10,
            spacingFactor: 1.5
        }).run();
    });
}

function hideDescendants(node) {
    const descendants = node.successors();
    descendants.forEach(function(ele) {
        ele.style('display', 'none');
    });
}

function showDescendants(node) {
    const children = node.outgoers('node');
    children.forEach(function(child) {
        child.style('display', 'element');
        // Also show edges to children
        const edges = node.edgesTo(child);
        edges.forEach(function(edge) {
            edge.style('display', 'element');
        });

        // If child is not collapsed, show its descendants too
        if (!collapsedNodes.has(child.id())) {
            showDescendants(child);
        }
    });
}
