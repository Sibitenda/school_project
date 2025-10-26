// import React from "react";
// import { NavigationContainer } from "@react-navigation/native";
// import { createStackNavigator } from "@react-navigation/stack";
// import LoginScreen from "./screens/LoginScreen";
// import DashboardScreen from "./screens/DashboardScreen";

// console.log("App.js loaded");  //  ADD THIS

// const Stack = createStackNavigator();

// export default function App() {
//   console.log(" Rendering App()");  //  ADD THIS
//   return (
//     <NavigationContainer>
//       <Stack.Navigator initialRouteName="Login">
//         <Stack.Screen name="Login" component={LoginScreen} />
//         <Stack.Screen name="Dashboard" component={DashboardScreen} />
//       </Stack.Navigator>
//     </NavigationContainer>
//   );
// }
import React from "react";
import { View, Text } from "react-native";

export default function App() {
  console.log("✅ App.js is running!");
  return (
    <View
      style={{
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
        backgroundColor: "#E3F2FD",
      }}
    >
      <Text style={{ fontSize: 24, color: "#1565C0" }}>
        ✅ Expo Frontend is working!
      </Text>
    </View>
  );
}

