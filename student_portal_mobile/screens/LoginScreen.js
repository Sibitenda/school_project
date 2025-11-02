import React, { useState } from "react";
import { View, Text, TextInput, Button, Alert, StyleSheet } from "react-native";
import { loginUser, fetchDashboard } from "../api/client";

export default function LoginScreen({ navigation }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  // const handleLogin = async () => {
  //   try {
  //     const tokenData = await loginUser(username, password);
  //     const token = tokenData?.access;

  //     if (!token) {
  //       throw new Error("Login failed — no token received");
  //     }

  //     const dashboardData = await fetchDashboard(token);

  //     // Convert role to lowercase for consistent comparison
  //     const role = dashboardData?.profile?.role?.toLowerCase();

  //     console.log(" Logged in as:", role);

  //     if (role === "admin") {
  //       navigation.navigate("AdminDashboard", { token });
  //     } else if (role === "lecturer") {
  //       navigation.navigate("LecturerDashboard", { token });
  //     } else {
  //       navigation.navigate("StudentDashboard", { token });
  //     }
  //   } catch (error) {
  //     console.error(error);
  //     Alert.alert("Error", "Invalid credentials or network issue.");
  //   }
  // };
  const handleLogin = async () => {
  try {
    const tokenData = await loginUser(username, password);
    const dashboardData = await fetchDashboard(tokenData.access);
    const role = dashboardData?.profile?.role?.toLowerCase();

    if (role === "admin") {
      navigation.replace("AdminDashboard", { token: tokenData.access });
    } else if (role === "lecturer") {
      navigation.replace("LecturerDashboard", { token: tokenData.access });
    } else {
      navigation.replace("StudentDashboard", { token: tokenData.access });
    }
  } catch (error) {
    console.error(error);
    Alert.alert("Login Failed", "Invalid credentials or server issue.");
  }
};



  return (
    <View style={styles.container}>
      <Text style={styles.title}> Student Progress - Login</Text>

      <TextInput
        style={styles.input}
        placeholder="Username"
        value={username}
        onChangeText={setUsername}
        autoCapitalize="none"
      />

      <TextInput
        style={styles.input}
        placeholder="Password"
        secureTextEntry
        value={password}
        onChangeText={setPassword}
      />

      <Button
        title={loading ? "Logging in..." : "Login"}
        onPress={handleLogin}
        disabled={loading}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    padding: 20,
    backgroundColor: "#f9f9f9",
  },
  title: {
    fontSize: 24,
    fontWeight: "bold",
    textAlign: "center",
    marginBottom: 20,
  },
  input: {
    borderWidth: 1,
    borderColor: "#ccc",
    padding: 10,
    marginBottom: 10,
    borderRadius: 8,
  },
});
