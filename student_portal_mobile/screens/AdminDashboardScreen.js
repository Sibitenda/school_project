import React, { useEffect, useState } from "react";
import { View, Text, Button, StyleSheet, ScrollView } from "react-native";
import { fetchDashboard } from "../api/client";

export default function AdminDashboardScreen({ route, navigation }) {
  const { token } = route.params;
  const [data, setData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetchDashboard(token);
        setData(res);
      } catch (err) {
        console.error(err);
      }
    };
    fetchData();
  }, []);

  if (!data) return <Text>Loading admin dashboard...</Text>;

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}> Admin Dashboard</Text>
      <Text>Name: {data.profile?.name}</Text>
      <Text>Role: {data.profile?.role}</Text>

      <View style={styles.card}>
        <Text style={styles.section}> Summary</Text>
        {Object.entries(data.summary || {}).map(([key, val]) => (
          <Text key={key}>{key}: {val}</Text>
        ))}
      </View>

      <Button title="Add New User" onPress={() => console.log("TODO: Add User")} />
      <Button title="Add Course" onPress={() => console.log("TODO: Add Course")} />
      <Button title="Enter Marks" onPress={() => console.log("TODO: Enter Marks")} />
      <Button title="Generate Reports" onPress={() => console.log("TODO: Generate Reports")} />

      <Button title="Logout" onPress={() => navigation.goBack()} color="red" />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, backgroundColor: "#fff" },
  title: { fontSize: 26, fontWeight: "bold", marginBottom: 15 },
  card: { backgroundColor: "#f4f4f4", padding: 10, borderRadius: 8, marginBottom: 15 },
  section: { fontWeight: "bold", fontSize: 18, marginBottom: 5 },
});
