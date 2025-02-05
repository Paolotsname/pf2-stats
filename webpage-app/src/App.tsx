// App.tsx
import React, { useState } from "react";
import "./styles.css";

// Import the separated components
import PickLevel from "./components/PickLevel";
import PickClass from "./components/PickClass";
import AttributeBonus from "./components/AttributeBonus";
import PickAverageType from "./components/PickAverageType"

interface Attributes {
    strengh: number;
    dexterity: number;
    constitution: number;
    intelligence: number;
    wisdom: number;
    charisma: number;
}

export default function App() {
    // Type the state variables
    const [playerLevel, setPlayerLevel] = useState<number>(0);
    const [enemyLevel, setEnemyLevel] = useState<number>(0);
    const [attributes, setAttributes] = useState<Attributes>({
        strengh: 0,
        dexterity: 0,
        constitution: 0,
        intelligence: 0,
        wisdom: 0,
        charisma: 0,
    });

    const handleAttributeChange = (attribute: keyof Attributes, value: number) => {
        setAttributes((prev) => ({ ...prev, [attribute]: value }));
    };

    return (
        <div>
            <div className="form-container">
                <PickLevel
                    label="Player Level"
                    value={playerLevel}
                    onChange={(e) => setPlayerLevel(Number(e.target.value))}
                />
                <AttributeBonus
                    label="Strengh"
                    value={attributes.strengh}
                    onChange={(e) => handleAttributeChange("strengh", Number(e.target.value))}
                />
                <AttributeBonus
                    label="Dexterity"
                    value={attributes.dexterity}
                    onChange={(e) => handleAttributeChange("dexterity", Number(e.target.value))}
                />
                <AttributeBonus
                    label="Constitution"
                    value={attributes.constitution}
                    onChange={(e) => handleAttributeChange("constitution", Number(e.target.value))}
                />
                <AttributeBonus
                    label="Intelligence"
                    value={attributes.intelligence}
                    onChange={(e) => handleAttributeChange("intelligence", Number(e.target.value))}
                />
                <AttributeBonus
                    label="Wisdom"
                    value={attributes.wisdom}
                    onChange={(e) => handleAttributeChange("wisdom", Number(e.target.value))}
                />
                <AttributeBonus
                    label="Charisma"
                    value={attributes.charisma}
                    onChange={(e) => handleAttributeChange("charisma", Number(e.target.value))}
                />
                <PickClass />
            </div>

            <div className="form-container">
                <PickLevel
                    label="Enemy level"
                    value={enemyLevel}
                    onChange={(e) => setEnemyLevel(Number(e.target.value))}
                />
                <PickAverageType />
            </div>
            <h3>amogus {playerLevel + enemyLevel}</h3>
        </div>
    );
}
