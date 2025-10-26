import React from "react";
import { View, Text } from "react-native";

export default function App() {
  console.log("✅ App.js loaded successfully!");
  return (
    <View style={{
      flex: 1,
      justifyContent: "center",
      alignItems: "center",
      backgroundColor: "#e3f2fd"
    }}>
      <Text style={{ fontSize: 24, color: "#1565c0" }}>✅ Expo App is running!</Text>
    </View>
  );
}
