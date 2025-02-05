import React from "react";

const PickClass = () => {
    return (
        <label>
            Pick a class:
            <select name="selectedClass">
                <option value="alchemist">Alchemist</option>
                <option value="ranger">Ranger</option>
            </select>
        </label>
    );
};

export default PickClass;
