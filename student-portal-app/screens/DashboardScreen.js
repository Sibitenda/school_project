import React, { useEffect, useState } from "react";
import { View, Text, Button, StyleSheet, ScrollView } from "react-native";
import { api } from "../api/client";

export default function DashboardScreen({ route, navigation }) {
  const { token } = route.params;
  const [data, setData] = useState(null);

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const response = await api.get("dashboard/", {
          headers: { Authorization: `Bearer ${token}` },
        });
        setData(response.data);
      } catch (error) {
        console.log(error);
      }
    };
    fetchDashboard();
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
