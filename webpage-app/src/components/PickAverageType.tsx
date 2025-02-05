import React from "react";

const PickClass = () => {
    return (
        <label>
            Pick a type of average:
            <select name="selectedClass">
                <option value="mean">mean</option>
                <option value="median">median</option>
                <option value="mode">mode</option>
            </select>
        </label>
    );
};

export default PickClass;
