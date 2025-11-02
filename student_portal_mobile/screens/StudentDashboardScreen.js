import React, { useEffect, useState } from "react";
import { View, Text, Button, StyleSheet, ScrollView } from "react-native";
import { fetchDashboard } from "../api/client";

export default function StudentDashboardScreen({ route, navigation }) {
  const { token } = route.params;
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetchDashboard(token);
        setData(res);
      } catch (err) {
        console.error("Dashboard fetch error:", err);
        setError("Failed to load dashboard data.");
      }
    };
    fetchData();
  }, []);

  if (error) {
    return (
      <View style={styles.container}>
        <Text style={styles.error}>{error}</Text>
        <Button title="Go Back" onPress={() => navigation.goBack()} />
      </View>
    );
  }

  if (!data) {
    return (
      <View style={styles.container}>
        <Text>Loading student dashboard...</Text>
      </View>
    );
  }

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>Student Dashboard</Text>

      {/* ✅ Safe access using optional chaining */}
      <Text>Name: {data.profile?.name || "N/A"}</Text>
      <Text>Role: {data.profile?.role || "N/A"}</Text>
      <Text>Courses: {data.courses?.length || 0}</Text>

      <Button title="Logout" onPress={() => navigation.goBack()} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, backgroundColor: "#fff" },
  title: { fontSize: 24, fontWeight: "bold", marginBottom: 10 },
  error: { color: "red", textAlign: "center", marginBottom: 20 },
});
