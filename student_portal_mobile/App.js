import * as React from "react";
import { NavigationContainer } from "@react-navigation/native";
import { createStackNavigator } from "@react-navigation/stack";

// Import your screens
import LoginScreen from "./screens/LoginScreen";
import AdminDashboardScreen from "./screens/AdminDashboardScreen";
import StudentDashboardScreen from "./screens/StudentDashboardScreen";
import LecturerDashboardScreen from "./screens/LecturerDashboardScreen";
import ManageUsersScreen from "./screens/ManageUsersScreen";

const Stack = createStackNavigator(); // Properly defined here

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Login">
        <Stack.Screen
          name="Login"
          component={LoginScreen}
          options={{ title: "Login" }}
        />
        <Stack.Screen
          name="AdminDashboard"
          component={AdminDashboardScreen}
          options={{ title: "Admin Dashboard" }}
        />
        <Stack.Screen
          name="StudentDashboard"
          component={StudentDashboardScreen}
          options={{ title: "Student Dashboard" }}
        />
        <Stack.Screen
          name="LecturerDashboard"
          component={LecturerDashboardScreen}
          options={{ title: "Lecturer Dashboard" }}
        />
        <Stack.Screen
          name="ManageUsers"
          component={ManageUsersScreen}
          options={{ title: "Manage Users" }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
