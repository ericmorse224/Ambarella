import React, { useState ***REMOVED*** from 'react';

export function ReviewPanel({ actions, onSubmit ***REMOVED***) {
    const [items, setItems] = useState(
        actions.map((action) => ({
            text: action,
            owner: '',
            startTime: new Date().toISOString().slice(0, 16),
            include: true,
        ***REMOVED***))
    );

    const updateItem = (index, updates) => {
        const newItems = [...items];
        newItems[index] = { ...newItems[index], ...updates ***REMOVED***;
        setItems(newItems);
    ***REMOVED***;

    const handleSubmit = () => {
        const filtered = items.filter((item) => item.include);
        onSubmit(filtered);
    ***REMOVED***;

    return (
        <div className="mt-6">
            <h2 className="text-xl font-semibold mb-4">Review and Schedule Actions</h2>
            {items.map((item, index) => (
                <div key={index***REMOVED*** className="border rounded p-4 mb-4 space-y-2">
                    <textarea
                        value={item.text***REMOVED***
                        onChange={(e) => updateItem(index, { text: e.target.value ***REMOVED***)***REMOVED***
                        className="w-full p-2 border border-gray-300 rounded"
                    />
                    <input
                        placeholder="Owner"
                        value={item.owner***REMOVED***
                        onChange={(e) => updateItem(index, { owner: e.target.value ***REMOVED***)***REMOVED***
                        className="w-full p-2 border border-gray-300 rounded"
                    />
                    <input
                        type="datetime-local"
                        value={item.startTime***REMOVED***
                        onChange={(e) => updateItem(index, { startTime: e.target.value ***REMOVED***)***REMOVED***
                        className="w-full p-2 border border-gray-300 rounded"
                    />
                    <div className="flex items-center space-x-2">
                        <input
                            type="checkbox"
                            checked={item.include***REMOVED***
                            onChange={(e) => updateItem(index, { include: e.target.checked ***REMOVED***)***REMOVED***
                        />
                        <span>Include this action</span>
                    </div>
                </div>
            ))***REMOVED***
            <button
                onClick={handleSubmit***REMOVED***
                className="mt-4 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
            >
                Schedule Selected
            </button>
        </div>
    );
***REMOVED***

export default ReviewPanel;
