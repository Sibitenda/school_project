import React, { useEffect, useState } from "react";
import { View, Text, Button, StyleSheet, ScrollView } from "react-native";
import { fetchDashboard } from "../api/client";

export default function DashboardScreen({ route, navigation }) {
  const { token } = route.params;
  const [data, setData] = useState(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        const result = await fetchDashboard(token);
        setData(result);
      } catch (error) {
        console.log("Dashboard fetch error:", error);
      }
    };
    loadData();
  }, []);

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>📘 Dashboard</Text>
      {data ? (
        <View>
          <Text>Name: {data.profile?.name}</Text>
          <Text>Role: {data.profile?.role}</Text>
          <Text>Courses: {data.courses?.length}</Text>
          <Text>Achievements: {data.achievements?.length}</Text>
        </View>
      ) : (
        <Text>Loading...</Text>
      )}
      <Button title="Logout" onPress={() => navigation.goBack()} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: "#fff",
  },
  title: {
    fontSize: 24,
    fontWeight: "bold",
    marginBottom: 10,
  },
});
