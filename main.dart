import 'package:flutter/material.dart';

import './homecreen.dart';

void main(List<String> args) {
  runApp(new appNew());
}

class appNew extends StatelessWidget {
  const appNew({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: HomeScreen(),
    );
  }
}
