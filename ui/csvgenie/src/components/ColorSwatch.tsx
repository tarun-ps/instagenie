const ColorSwatch = ({ colors }: { colors: any[] }) => {
    return (
      <div style={{ display: "flex", gap: "8px", padding: "10px" }}>
        {colors.map((color: any, index: number) => (
          <div key={index} style={{ textAlign: "center" }}>
            <div
              style={{
                width: "10px",
                height: "10px",
                backgroundColor: color,
                borderRadius: "1px",
                border: "1px solid #ccc",
              }}
            ></div>
          </div>
        ))}
      </div>
    );
  };
  
  export default ColorSwatch;