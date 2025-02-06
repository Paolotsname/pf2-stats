import React, { useState } from "react";
import "./styles.css";

import PickLevel from "./components/PickLevel";
import PickClass from "./components/PickClass";
import AttributeBonus from "./components/AttributeBonus";
import PickAverageType from "./components/PickAverageType"

export default function App() {
    const [playerLevel, setPlayerLevel] = useState<number>(0);
    const [enemyLevel, setEnemyLevel] = useState<number>(0);
    const [strengh, setStrengh] = useState<number>(0);
    const [dexterity, setDexterity] = useState<number>(0);
    const [constitution, setConstitution] = useState<number>(0);
    const [intelligence, setIntelligence] = useState<number>(0);
    const [wisdom, setWisdom] = useState<number>(0);
    const [charisma, setCharisma] = useState<number>(0);
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
                    value={strengh}
                    onChange={(e) => setStrengh(Number(e.target.value))}
                />
                <AttributeBonus
                    label="Dexterity"
                    value={dexterity}
                    onChange={(e) => setDexterity(Number(e.target.value))}
                />
                <AttributeBonus
                    label="Constitution"
                    value={constitution}
                    onChange={(e) => setConstitution(Number(e.target.value))}
                />
                <AttributeBonus
                    label="Intelligence"
                    value={intelligence}
                    onChange={(e) => setIntelligence(Number(e.target.value))}
                />
                <AttributeBonus
                    label="Wisdom"
                    value={wisdom}
                    onChange={(e) => setWisdom(Number(e.target.value))}
                />
                <AttributeBonus
                    label="Charisma"
                    value={charisma}
                    onChange={(e) => setCharisma(Number(e.target.value))}
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
        </div>
    );
}
