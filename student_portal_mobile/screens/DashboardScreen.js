import React, { useEffect, useState } from "react";
import { View, Text, Button, StyleSheet, ScrollView } from "react-native";
import { fetchDashboard } from "../api/client";

export default function DashboardScreen({ route, navigation }) {
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

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>📘 Dashboard</Text>
      {data ? (
        <>
          <Text>Name: {data.profile?.name}</Text>
          <Text>Role: {data.profile?.role}</Text>
          <Text>Courses: {data.courses?.length}</Text>
        </>
      ) : (
        <Text>Loading...</Text>
      )}
      <Button title="Logout" onPress={() => navigation.goBack()} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, backgroundColor: "#fff" },
  title: { fontSize: 24, fontWeight: "bold", marginBottom: 10 },
});
