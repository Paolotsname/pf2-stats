import React, { ChangeEvent } from "react";

// Define the type for the PickLevel component's props
interface PickLevelProps {
    label: string;
    value: number;
    onChange: (e: ChangeEvent<HTMLInputElement>) => void;
}

const PickLevel = ({ label, value, onChange }: PickLevelProps) => {
    return (
        <label>
            {label}:
            <input type="number" value={value} onChange={onChange} />
        </label>
    );
};

export default PickLevel;
